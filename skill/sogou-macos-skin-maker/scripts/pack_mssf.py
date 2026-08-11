#!/usr/bin/env python3
"""Pack a Sogou macOS skin folder into the nested .mssf structure."""

from __future__ import annotations

import argparse
import io
import plistlib
from pathlib import Path
import zipfile


SKIP_NAMES = {".DS_Store"}
FIXED_TIME = (2020, 1, 1, 0, 0, 0)


def zip_info(name: str) -> zipfile.ZipInfo:
    info = zipfile.ZipInfo(name, FIXED_TIME)
    info.compress_type = zipfile.ZIP_DEFLATED
    info.external_attr = 0o100644 << 16
    return info


def collect_files(root: Path) -> list[Path]:
    files = []
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        rel = path.relative_to(root)
        if any(part == "__MACOSX" for part in rel.parts) or path.name in SKIP_NAMES:
            continue
        files.append(path)
    return sorted(files, key=lambda p: p.relative_to(root).as_posix())


def pack(inner_dir: Path, output: Path) -> None:
    plist_path = inner_dir / "skin.plist"
    if not plist_path.is_file():
        raise SystemExit(f"missing {plist_path}")
    with plist_path.open("rb") as fh:
        plistlib.load(fh)

    inner_bytes = io.BytesIO()
    with zipfile.ZipFile(inner_bytes, "w") as inner_zip:
        for path in collect_files(inner_dir):
            rel = path.relative_to(inner_dir).as_posix()
            inner_zip.writestr(zip_info(rel), path.read_bytes())

    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "w") as outer_zip:
        outer_zip.writestr(zip_info("Skin"), inner_bytes.getvalue())

    with zipfile.ZipFile(output) as outer_zip:
        if outer_zip.namelist() != ["Skin"]:
            raise SystemExit("outer archive must contain exactly one member named Skin")
        with zipfile.ZipFile(io.BytesIO(outer_zip.read("Skin"))) as inner_zip:
            if "skin.plist" not in inner_zip.namelist():
                raise SystemExit("inner archive is missing skin.plist")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("inner_dir", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    pack(args.inner_dir.resolve(), args.output.resolve())
    print(args.output.resolve())


if __name__ == "__main__":
    main()

