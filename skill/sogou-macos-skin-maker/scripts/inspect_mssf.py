#!/usr/bin/env python3
"""Inspect nested Sogou .mssf packages without extracting them to disk."""

from __future__ import annotations

import argparse
import io
import json
from pathlib import Path
import plistlib
import struct
import zipfile
import zlib


PNG_SIG = b"\x89PNG\r\n\x1a\n"


def paeth(a: int, b: int, c: int) -> int:
    p = a + b - c
    pa, pb, pc = abs(p - a), abs(p - b), abs(p - c)
    return a if pa <= pb and pa <= pc else b if pb <= pc else c


def png_fully_transparent(data: bytes, width: int, height: int) -> bool | None:
    """Return alpha emptiness for common 8-bit grayscale-alpha/RGBA PNGs."""
    pos = 8
    bit_depth = color_type = None
    compressed = []
    while pos + 12 <= len(data):
        length = struct.unpack(">I", data[pos : pos + 4])[0]
        kind = data[pos + 4 : pos + 8]
        payload = data[pos + 8 : pos + 8 + length]
        if kind == b"IHDR":
            bit_depth, color_type = payload[8], payload[9]
        elif kind == b"IDAT":
            compressed.append(payload)
        pos += length + 12
        if kind == b"IEND":
            break
    channels = {4: 2, 6: 4}.get(color_type)
    if bit_depth != 8 or channels is None or not compressed:
        return None
    raw = zlib.decompress(b"".join(compressed))
    stride = width * channels
    previous = bytearray(stride)
    cursor = 0
    for _ in range(height):
        filter_type = raw[cursor]
        cursor += 1
        encoded = raw[cursor : cursor + stride]
        cursor += stride
        current = bytearray(stride)
        for index, value in enumerate(encoded):
            left = current[index - channels] if index >= channels else 0
            up = previous[index]
            upper_left = previous[index - channels] if index >= channels else 0
            if filter_type == 0:
                decoded = value
            elif filter_type == 1:
                decoded = value + left
            elif filter_type == 2:
                decoded = value + up
            elif filter_type == 3:
                decoded = value + ((left + up) // 2)
            elif filter_type == 4:
                decoded = value + paeth(left, up, upper_left)
            else:
                return None
            current[index] = decoded & 0xFF
        if any(current[index] for index in range(channels - 1, stride, channels)):
            return False
        previous = current
    return True


def png_info(data: bytes) -> dict | None:
    if not data.startswith(PNG_SIG) or len(data) < 33:
        return None
    width, height = struct.unpack(">II", data[16:24])
    pos = 8
    chunks = []
    frames = None
    plays = None
    while pos + 12 <= len(data):
        length = struct.unpack(">I", data[pos : pos + 4])[0]
        kind = data[pos + 4 : pos + 8].decode("ascii", "replace")
        payload = data[pos + 8 : pos + 8 + length]
        chunks.append(kind)
        if kind == "acTL" and len(payload) == 8:
            frames, plays = struct.unpack(">II", payload)
        pos += length + 12
        if kind == "IEND":
            break
    result = {"width": width, "height": height}
    transparent = png_fully_transparent(data, width, height)
    if transparent is not None:
        result["fully_transparent"] = transparent
    if frames is not None:
        result["apng_frames"] = frames
        result["apng_plays"] = plays
        result["frame_controls"] = chunks.count("fcTL")
    return result


def nested_get(mapping: dict, *keys):
    current = mapping
    for key in keys:
        if not isinstance(current, dict):
            return None
        current = current.get(key)
    return current


def inspect(path: Path) -> dict:
    warnings = []
    with zipfile.ZipFile(path) as outer:
        outer_members = outer.namelist()
        if outer_members != ["Skin"]:
            warnings.append("outer archive should contain exactly one member named Skin")
        if "Skin" not in outer_members:
            raise SystemExit("missing outer Skin member")
        inner_data = outer.read("Skin")

    with zipfile.ZipFile(io.BytesIO(inner_data)) as inner:
        members = inner.namelist()
        if "skin.plist" not in members:
            raise SystemExit("inner archive is missing skin.plist")
        plist = plistlib.loads(inner.read("skin.plist"))
        images = {}
        for name in members:
            if name.lower().endswith(".png"):
                images[name] = png_info(inner.read(name))

    for name, info in images.items():
        if "@2x" in name or not info:
            continue
        retina = name[:-4] + "@2x.png"
        if retina in images and images[retina]:
            if images[retina]["width"] != info["width"] * 2 or images[retina]["height"] != info["height"] * 2:
                warnings.append(f"{retina} is not exactly double {name}")

    referenced = set()
    def walk(value):
        if isinstance(value, dict):
            for key, child in value.items():
                if key == "ImgName" and isinstance(child, str):
                    referenced.add(child)
                walk(child)
        elif isinstance(value, list):
            for child in value:
                walk(child)
    walk(plist)
    missing = sorted(name for name in referenced if name not in members)
    if missing:
        warnings.append("missing referenced assets: " + ", ".join(missing))

    transparent_pages = [
        (name, info) for name, info in images.items()
        if name.startswith(("pageup_", "pagedown_")) and info and info.get("fully_transparent")
    ]
    oversized_pages = [name for name, info in transparent_pages if info["width"] > 4 or info["height"] > 4]
    if oversized_pages:
        warnings.append(
            "fully transparent page assets may still reserve runtime space; "
            "use minimal canvases or calibrate FontSetting/Page padding: " + ", ".join(sorted(oversized_pages))
        )

    humming = nested_get(plist, "NotificationInfo", "HummingNotif") or []
    return {
        "path": str(path),
        "outer_members": outer_members,
        "inner_file_count": len(members),
        "skin_name": nested_get(plist, "AdditionalInfo", "SkinName"),
        "trunk_image": nested_get(plist, "SkinInfo", "TrunkImageInfo", "ImgNode", "ImgName"),
        "trunk_offset": nested_get(plist, "SkinInfo", "TrunkImageInfo", "CurOffset"),
        "stretch_center": nested_get(plist, "SkinInfo", "TrunkImageInfo", "ImgNode", "StretchCenter"),
        "font_padding": nested_get(plist, "SkinInfo", "FontSetting", "Padding"),
        "page_up_padding": nested_get(plist, "SkinInfo", "PageUpInfo", "Padding"),
        "page_down_padding": nested_get(plist, "SkinInfo", "PageDownInfo", "Padding"),
        "humming_states": len(humming),
        "images": images,
        "warnings": warnings,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=Path)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = inspect(args.path.resolve())
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return
    print(f"Skin: {result['skin_name']}")
    print(f"Files: {result['inner_file_count']}")
    print(f"Trunk: {result['trunk_image']} offset={result['trunk_offset']} stretch={result['stretch_center']}")
    print(
        "Padding: "
        f"font={result['font_padding']} page-up={result['page_up_padding']} page-down={result['page_down_padding']}"
    )
    print(f"Humming states: {result['humming_states']}")
    for name, info in result["images"].items():
        if info and ("apng_frames" in info or name in {result["trunk_image"], "chars_0.png", "chars_0@2x.png"}):
            print(f"  {name}: {info}")
    if result["warnings"]:
        print("Warnings:")
        for warning in result["warnings"]:
            print(f"  - {warning}")


if __name__ == "__main__":
    main()
