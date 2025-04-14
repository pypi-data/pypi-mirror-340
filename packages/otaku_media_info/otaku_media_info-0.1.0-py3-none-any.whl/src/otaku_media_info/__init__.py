# coding: utf-8

from pathlib import Path

import pymediainfo

from . import bangumi


def parse(
    file_path: Path,
) -> None:
    if not file_path.exists():
        raise ValueError("File does not exist")

    file_size = file_path.stat().st_size
    if file_size == 0:
        raise ValueError("File is empty")

    ext = file_path.suffix.lower()

    if ext in [".mp4", ".mkv"]:
        return bangumi.parse(file_path)

    raise NotImplementedError(f"Unsupported file type: {ext}")
