from __future__ import annotations

import importlib.util
import io
from pathlib import Path
import plistlib
import struct
import tempfile
import unittest
import zipfile
import zlib


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skill" / "sogou-macos-skin-maker"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def png_rgba(red: int, green: int, blue: int, alpha: int = 255) -> bytes:
    signature = b"\x89PNG\r\n\x1a\n"

    def chunk(kind: bytes, payload: bytes) -> bytes:
        crc = zlib.crc32(kind + payload) & 0xFFFFFFFF
        return struct.pack(">I", len(payload)) + kind + payload + struct.pack(">I", crc)

    ihdr = struct.pack(">IIBBBBB", 1, 1, 8, 6, 0, 0, 0)
    raw = bytes((0, red, green, blue, alpha))
    return signature + chunk(b"IHDR", ihdr) + chunk(b"IDAT", zlib.compress(raw)) + chunk(b"IEND", b"")


class SkillPackageTests(unittest.TestCase):
    def test_metadata_and_public_safety(self) -> None:
        skill_md = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        self.assertTrue(skill_md.startswith("---\n"))
        self.assertIn("\nname: sogou-macos-skin-maker\n", skill_md)
        self.assertIn("$sogou-macos-skin-maker", (SKILL / "agents" / "openai.yaml").read_text())

        forbidden_suffixes = {".ssf", ".mssf"}
        forbidden_text = ("/Users/", "/var/folders/", "/private/tmp/", "BEGIN PRIVATE KEY")
        for path in SKILL.rglob("*"):
            if not path.is_file():
                continue
            self.assertNotIn(path.suffix.lower(), forbidden_suffixes, path)
            text = path.read_text(encoding="utf-8")
            for marker in forbidden_text:
                self.assertNotIn(marker, text, path)

    def test_tools_compile(self) -> None:
        for path in (SKILL / "scripts").glob("*.py"):
            compile(path.read_text(encoding="utf-8"), str(path), "exec")

    def test_mssf_pack_and_inspect_round_trip(self) -> None:
        packer = load_module("pack_mssf", SKILL / "scripts" / "pack_mssf.py")
        inspector = load_module("inspect_mssf", SKILL / "scripts" / "inspect_mssf.py")
        with tempfile.TemporaryDirectory() as tmp:
            temp = Path(tmp)
            inner = temp / "skin"
            inner.mkdir()
            plist = {
                "AdditionalInfo": {"SkinName": "Test Skin"},
                "SkinInfo": {
                    "TrunkImageInfo": {
                        "ImgNode": {"ImgName": "skin.png", "StretchCenter": "0,0,1,1"},
                        "CurOffset": "0,0",
                    },
                    "FontSetting": {"Padding": "0,0,0,0"},
                },
            }
            (inner / "skin.plist").write_bytes(plistlib.dumps(plist))
            (inner / "skin.png").write_bytes(png_rgba(255, 128, 128))
            package = temp / "test.mssf"
            packer.pack(inner, package)
            result = inspector.inspect(package)
            self.assertEqual(result["outer_members"], ["Skin"])
            self.assertEqual(result["skin_name"], "Test Skin")
            self.assertEqual(result["images"]["skin.png"]["width"], 1)

    def test_apng_assemble_and_inspect(self) -> None:
        apng = load_module("apng_tool", SKILL / "scripts" / "apng_tool.py")
        with tempfile.TemporaryDirectory() as tmp:
            temp = Path(tmp)
            frames = [temp / "frame0.png", temp / "frame1.png"]
            frames[0].write_bytes(png_rgba(255, 0, 0))
            frames[1].write_bytes(png_rgba(0, 0, 255))
            output = temp / "animation.png"
            apng.assemble(frames, output, 1, 10, 0)
            result = apng.inspect(output)
            self.assertEqual(result["frames"], 2)
            self.assertEqual(result["plays"], 0)
            self.assertEqual(len(result["frame_controls"]), 2)


if __name__ == "__main__":
    unittest.main()
