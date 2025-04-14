# coding: utf-8

from pathlib import Path

from . import parse

if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python -m otaku_media_info <file_path>")
        sys.exit(1)

    file_path = Path(sys.argv[1])
    result = parse(file_path)

    print(result)
