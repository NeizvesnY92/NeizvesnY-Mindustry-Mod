#!/usr/bin/env python3
"""Validate Mindustry block sprite footprints and required Russian localization."""

import argparse
import re
import struct
from pathlib import Path
from typing import List, Optional, Set, Tuple


PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
TILE_PIXELS = 32


def png_dimensions(path: Path) -> Tuple[int, int]:
    with path.open("rb") as stream:
        header = stream.read(24)
    if len(header) != 24 or header[:8] != PNG_SIGNATURE or header[12:16] != b"IHDR":
        raise ValueError("not a valid PNG with an IHDR header")
    width, height = struct.unpack(">II", header[16:24])
    if width == 0 or height == 0:
        raise ValueError("PNG has an empty dimension")
    return width, height


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
