from __future__ import annotations

from datetime import UTC, datetime, timedelta
import os
from collections.abc import Sequence
from io import BytesIO
from pathlib import Path
from typing import Any

import sh

from .status import get_status


class Repo:
    def __init__(
        self, path: Path | str,
        *,
        user_name: str,
        user_email: str,
    ) -> None:
        self.__path: Path = Path(path).expanduser()

        self.__git = sh.bake(
            _cwd=self.__path,
            _env={
                "GIT_AUTHOR_NAME": user_name,
                "GIT_AUTHOR_EMAIL": user_email,
                "GIT_COMMITTER_NAME": user_name,
                "GIT_COMMITTER_EMAIL": user_email,
            } | os.environ,
        ).git

        if not (self.__path / ".git").is_dir():
            msg = "Specified path must be part of a Git repo."
            raise ValueError(msg)

    @staticmethod
    def init(
        path: Path | str,
        *,
        exist_ok: bool = True,
        **kwargs: Any,
    ) -> Repo:
        repo_path: Path = Path(path).expanduser()

        repo_path.mkdir(parents=True, exist_ok=True)

        if (repo_path / ".git").exists():
            if not exist_ok:
                msg = "Specified path is already a Git repo."
                raise RuntimeError(msg)
        else:
            sh.git(
                "init",
                _cwd=repo_path,
            )

        return Repo(repo_path, **kwargs)

    def is_clean(self) -> bool:
        status: dict[str, Any] | None = get_status(str(self.__path))
        if not status:
            msg = "Cannot get status of Git repo."
            raise RuntimeError(msg)

        return not (status["files"]["staged"] or status["files"]["unstaged"])

    def stage(self, *files: str) -> None:
        args: list[str] = ["--", *files] if files else ["."]

        self.__git(
            "add", *args,
        )

    def reset(self) -> None:
        self.__git(
            "reset",
        )

    def commit(self, message: str, *, stage_all: bool = True, background: bool = False) -> None:
        args: list[str] = ["--all"] if stage_all else []

        self.__git(
            "commit", *args, f"--message={message}",
            _bg=background,
        )

    def pull(self, *, rebase: bool = True, background: bool = False) -> None:
        if not self.is_clean():
            msg = "Repo is not clean."
            raise RuntimeError(msg)

        args: list[str] = ["--rebase=true"] if rebase else []

        self.__git(
            "pull", *args,
            _bg=background,
        )

    def push(self, *, background: bool = False) -> None:
        if not self.is_clean():
            msg = "Repo is not clean."
            raise RuntimeError(msg)

        self.__git(
            "push",
            _bg=background,
        )

    def list_commits(
        self,
        relative_path: Path | str | None = None,
        *,
        max_count: int | None = None,
        before: datetime | timedelta | None = None,
    ) -> Sequence[str]:
        args: list[str] = []

        if before:
            if isinstance(before, timedelta):
                before = datetime.now(UTC) - before

            args.append(f"--before={before.isoformat()}")

        if max_count:
            args.append(f"--max-count={max_count}")

        if relative_path:
            args.append(str(relative_path))

        output: str = self.__git(
            "log", "--oneline", "--reverse", *args,
            _tty_out=False,
        )

        return [
            line.split(' ')[0]
            for line in output.strip().splitlines()
        ]

    def get_blob(
        self,
        relative_path: Path | str,
        *,
        version: str | int | datetime | timedelta | None = None,
    ) -> bytes:
        blob_path: Path = self.__path / relative_path

        try:
            if version is None:
                return blob_path.read_bytes()

            if isinstance(version, int):
                commits: Sequence[str] = self.list_commits(
                    relative_path,
                    max_count=(-version if version < 0 else None),
                )

                version = commits[version]
            elif isinstance(version, (datetime, timedelta)):
                commits: Sequence[str] = self.list_commits(
                    relative_path,
                    max_count=1,
                    before=version,
                )

                version = commits[0]

            bio = BytesIO()
            self.__git(
                "show", f"{version}:{relative_path}",
                _out=bio,
                _tty_out=False,
            )
            return bio.getvalue()
        except Exception as e:
            raise FileNotFoundError from e
