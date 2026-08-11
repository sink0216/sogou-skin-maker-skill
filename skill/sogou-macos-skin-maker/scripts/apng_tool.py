#!/usr/bin/env python3
"""Inspect or assemble full-frame APNG animations using only the standard library."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import struct
import zlib


PNG_SIG = b"\x89PNG\r\n\x1a\n"


def chunks(data: bytes):
    if not data.startswith(PNG_SIG):
        raise ValueError("not a PNG")
    pos = 8
    while pos + 12 <= len(data):
        length = struct.unpack(">I", data[pos : pos + 4])[0]
        kind = data[pos + 4 : pos + 8]
        payload = data[pos + 8 : pos + 8 + length]
        yield kind, payload
        pos += length + 12
        if kind == b"IEND":
            break


def chunk(kind: bytes, payload: bytes) -> bytes:
    crc = zlib.crc32(kind + payload) & 0xFFFFFFFF
    return struct.pack(">I", len(payload)) + kind + payload + struct.pack(">I", crc)


def inspect(path: Path) -> dict:
    data = path.read_bytes()
    result = {"path": str(path), "chunks": [], "frames": None, "plays": None, "frame_controls": []}
    for kind, payload in chunks(data):
        name = kind.decode("ascii")
        result["chunks"].append(name)
        if kind == b"IHDR":
            result["width"], result["height"] = struct.unpack(">II", payload[:8])
        elif kind == b"acTL":
            result["frames"], result["plays"] = struct.unpack(">II", payload)
        elif kind == b"fcTL":
            seq, width, height, x, y, num, den, dispose, blend = struct.unpack(">IIIIIHHBB", payload)
            result["frame_controls"].append({
                "sequence": seq, "width": width, "height": height, "x": x, "y": y,
                "delay_num": num, "delay_den": den, "dispose": dispose, "blend": blend,
            })
    return result


def assemble(frame_paths: list[Path], output: Path, delay_num: int, delay_den: int, plays: int) -> None:
    if len(frame_paths) < 2:
        raise SystemExit("APNG requires at least two frames")
    frames = [path.read_bytes() for path in frame_paths]
    parsed = [list(chunks(frame)) for frame in frames]
    ihdrs = [next(payload for kind, payload in item if kind == b"IHDR") for item in parsed]
    if any(header != ihdrs[0] for header in ihdrs[1:]):
        raise SystemExit("all frames must have identical IHDR data")
    width, height = struct.unpack(">II", ihdrs[0][:8])
    phys = next((payload for kind, payload in parsed[0] if kind == b"pHYs"), None)

    output_parts = [PNG_SIG, chunk(b"IHDR", ihdrs[0])]
    if phys is not None:
        output_parts.append(chunk(b"pHYs", phys))
    output_parts.append(chunk(b"acTL", struct.pack(">II", len(frames), plays)))

    sequence = 0
    for index, frame_chunks in enumerate(parsed):
        control = struct.pack(
            ">IIIIIHHBB", sequence, width, height, 0, 0,
            delay_num, delay_den, 0, 0,
        )
        sequence += 1
        output_parts.append(chunk(b"fcTL", control))
        idats = [payload for kind, payload in frame_chunks if kind == b"IDAT"]
        if not idats:
            raise SystemExit(f"{frame_paths[index]} has no IDAT chunks")
        if index == 0:
            output_parts.extend(chunk(b"IDAT", payload) for payload in idats)
        else:
            for payload in idats:
                output_parts.append(chunk(b"fdAT", struct.pack(">I", sequence) + payload))
                sequence += 1
    output_parts.append(chunk(b"IEND", b""))
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(b"".join(output_parts))


def main() -> None:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    inspect_parser = sub.add_parser("inspect")
    inspect_parser.add_argument("path", type=Path)
    assemble_parser = sub.add_parser("assemble")
    assemble_parser.add_argument("frames", nargs="+", type=Path)
    assemble_parser.add_argument("-o", "--output", required=True, type=Path)
    assemble_parser.add_argument("--delay-num", type=int, default=28)
    assemble_parser.add_argument("--delay-den", type=int, default=100)
    assemble_parser.add_argument("--plays", type=int, default=0)
    args = parser.parse_args()

    if args.command == "inspect":
        print(json.dumps(inspect(args.path.resolve()), indent=2))
    else:
        assemble(args.frames, args.output, args.delay_num, args.delay_den, args.plays)
        print(json.dumps(inspect(args.output.resolve()), indent=2))


if __name__ == "__main__":
    main()

