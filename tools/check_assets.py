#!/usr/bin/env python3
"""Validate Mindustry block sprite footprints and required Russian localization."""

import argparse
import re
import struct
import zlib
from pathlib import Path
from typing import List, Optional, Set, Tuple


PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
TILE_PIXELS = 32
PNG_CHUNK_LIMIT = 64 * 1024


def read_exact(stream, size: int, label: str) -> bytes:
    data = stream.read(size)
    if len(data) != size:
        raise ValueError(f"truncated PNG {label}")
    return data


def read_chunk_payload(stream, chunk_type: bytes, length: int) -> None:
    """Consume a chunk without loading large ancillary chunks into memory."""
    checksum = zlib.crc32(chunk_type)
    remaining = length
    while remaining:
        data = stream.read(min(PNG_CHUNK_LIMIT, remaining))
        if not data:
            raise ValueError(
                f"truncated PNG {chunk_type.decode('ascii', errors='replace')} chunk data"
            )
        checksum = zlib.crc32(data, checksum)
        remaining -= len(data)

    expected = struct.unpack(">I", read_exact(stream, 4, "chunk CRC"))[0]
    if checksum & 0xFFFFFFFF != expected:
        raise ValueError(
            f"PNG {chunk_type.decode('ascii', errors='replace')} chunk CRC mismatch"
        )


def png_dimensions(path: Path) -> Tuple[int, int]:
    """Return PNG dimensions only after validating its chunk structure and CRCs."""
    with path.open("rb") as stream:
        if read_exact(stream, 8, "signature") != PNG_SIGNATURE:
            raise ValueError("not a PNG file")

        width = height = color_type = None
        seen_ihdr = False
        seen_plte = False
        seen_idat = False
        idat_ended = False
        idat_bytes = 0

        while True:
            header = read_exact(stream, 8, "chunk header")
            length, chunk_type = struct.unpack(">I4s", header)

            if any(not (65 <= byte <= 90 or 97 <= byte <= 122) for byte in chunk_type):
                raise ValueError("PNG chunk type contains non-letter bytes")
            if chunk_type[2] & 0x20:
                raise ValueError("PNG chunk type uses the reserved lowercase bit")

            if not seen_ihdr and chunk_type != b"IHDR":
                raise ValueError("PNG IHDR must be the first chunk")
            if chunk_type == b"IHDR":
                if seen_ihdr or length != 13:
                    raise ValueError("PNG must contain exactly one 13-byte IHDR")
                data = read_exact(stream, length, "IHDR data")
                checksum = zlib.crc32(chunk_type)
                checksum = zlib.crc32(data, checksum) & 0xFFFFFFFF
                expected = struct.unpack(">I", read_exact(stream, 4, "IHDR CRC"))[0]
                if checksum != expected:
                    raise ValueError("PNG IHDR chunk CRC mismatch")

                width, height, bit_depth, color_type, compression, filtering, interlace = (
                    struct.unpack(">IIBBBBB", data)
                )
                if not (1 <= width <= 0x7FFFFFFF and 1 <= height <= 0x7FFFFFFF):
                    raise ValueError("PNG has an invalid dimension")
                valid_depths = {
                    0: {1, 2, 4, 8, 16},
                    2: {8, 16},
                    3: {1, 2, 4, 8},
                    4: {8, 16},
                    6: {8, 16},
                }
                if color_type not in valid_depths or bit_depth not in valid_depths[color_type]:
                    raise ValueError("PNG has an invalid bit-depth/color-type combination")
                if compression != 0 or filtering != 0 or interlace not in (0, 1):
                    raise ValueError("PNG uses an unsupported IHDR method")
                seen_ihdr = True
                continue

            if chunk_type == b"PLTE":
                if seen_plte or seen_idat or length == 0 or length % 3 or length > 768:
                    raise ValueError("PNG has an invalid or misplaced PLTE chunk")
                if color_type in (0, 4):
                    raise ValueError("PNG color type does not permit a PLTE chunk")
                seen_plte = True
            elif chunk_type == b"IDAT":
                if idat_ended:
                    raise ValueError("PNG IDAT chunks must be consecutive")
                seen_idat = True
                idat_bytes += length
            else:
                if seen_idat:
                    idat_ended = True
                if chunk_type == b"IEND":
                    if length != 0:
                        raise ValueError("PNG IEND chunk must be empty")
                    if not seen_idat or idat_bytes == 0:
                        raise ValueError("PNG is missing image data")
                    read_chunk_payload(stream, chunk_type, length)
                    if stream.read(1):
                        raise ValueError("PNG contains data after IEND")
                    if color_type == 3 and not seen_plte:
                        raise ValueError("indexed PNG is missing its PLTE palette")
                    return width, height
                if chunk_type[0] & 0x20 == 0 and chunk_type != b"PLTE":
                    raise ValueError(
                        f"PNG contains unknown critical chunk {chunk_type.decode('ascii')}"
                    )

            read_chunk_payload(stream, chunk_type, length)


def top_level_value(text: str, field: str) -> Optional[str]:
    matches = re.findall(rf"(?m)^{re.escape(field)}:\s*([^\s#]+)\s*(?:#.*)?$", text)
    return matches[0] if len(matches) == 1 else None


def property_keys(path: Path) -> Set[str]:
    keys = set()
    for line in path.read_text(encoding="utf-8-sig").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith(("#", "!")):
            continue
        key, separator, _ = stripped.partition("=")
        if separator:
            keys.add(key.strip())
    return keys


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--mod",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="mod root containing mod.hjson (default: repository root)",
    )
    args = parser.parse_args()
    root = args.mod.resolve(strict=True)
    errors: List[str] = []

    metadata = root / "mod.hjson"
    if not metadata.is_file():
        parser.error("--mod must contain mod.hjson")
    mod_name = top_level_value(metadata.read_text(encoding="utf-8"), "name")
    if not mod_name:
        print("FAIL: mod.hjson must contain exactly one top-level name")
        return 1

    block_dir = root / "content" / "blocks"
    definitions = sorted(block_dir.glob("*.hjson")) if block_dir.is_dir() else []
    if not definitions:
        print("FAIL: no content/blocks/*.hjson definitions found")
        return 1

    required_keys: Set[str] = set()
    for definition in definitions:
        stem = definition.stem
        text = definition.read_text(encoding="utf-8")
        raw_size = top_level_value(text, "size")
        if raw_size is None or not raw_size.isdigit() or int(raw_size) < 1:
            errors.append(f"{definition.relative_to(root)}: missing or invalid top-level size")
            continue

        if not re.search(r"(?m)^name:\s*\S", text):
            errors.append(f"{definition.relative_to(root)}: missing top-level name")
        if not re.search(r"(?m)^description:\s*\S", text):
            errors.append(f"{definition.relative_to(root)}: missing top-level description")

        expected = int(raw_size) * TILE_PIXELS
        sprite_paths = [root / "sprites" / "blocks" / f"{stem}.png"]
        base_sprite = root / "sprites" / "blocks" / f"{stem}-base.png"
        block_type = top_level_value(text, "type")
        requires_base = block_type == "ItemTurret" and top_level_value(text, "hasBase") != "false"
        if requires_base or base_sprite.exists():
            sprite_paths.append(base_sprite)

        for sprite in sprite_paths:
            rel = sprite.relative_to(root)
            if not sprite.is_file():
                errors.append(f"{rel}: required block sprite is missing")
                continue
            try:
                actual = png_dimensions(sprite)
            except (OSError, ValueError) as error:
                errors.append(f"{rel}: {error}")
                continue
            if actual != (expected, expected):
                errors.append(
                    f"{rel}: {actual[0]}x{actual[1]} px; size {raw_size} requires "
                    f"{expected}x{expected} px ({TILE_PIXELS} px per tile)"
                )
            else:
                print(f"OK: {rel} = {actual[0]}x{actual[1]} px")

        prefix = f"block.{mod_name}-{stem}"
        required_keys.update((f"{prefix}.name", f"{prefix}.description"))

    for bundle_name in ("bundle_ru.properties", "bundle_ru_RU.properties"):
        bundle = root / "bundles" / bundle_name
        if not bundle.is_file():
            errors.append(f"bundles/{bundle_name}: required Russian bundle is missing")
            continue
        missing = sorted(required_keys - property_keys(bundle))
        if missing:
            errors.append(f"bundles/{bundle_name}: missing keys: {', '.join(missing)}")
        else:
            print(f"OK: bundles/{bundle_name} contains all {len(required_keys)} required block keys")

    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        return 1

    print(f"MOD_ASSETS_PASS: {len(definitions)} block sprites and Russian localization bundles")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
