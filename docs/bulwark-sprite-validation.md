# Bulwark 2x2 sprite correction — 2026-11-12

Base: daily/sentinel-graphite-impact-20261111 at 6414dd203e5bb688c4717260c138913b772dd8a7. The main branch remains unchanged. This branch carries the existing experimental test build plus one new visual correction.

## Finding and change

The Bulwark definition has size: 2, but sprites/blocks/neizvesny-bulwark.png was the same 32x32 image as the 1x1 Wall. Mindustry's block sprite convention is 32 pixels per tile, so the 2x2 Bulwark needs a 64x64 texture. Replaced only the Bulwark sprite with a dedicated 64x64 pixel-art heavy wall: charcoal steel plates, beveled armor, and orange cross-bracing matching the existing Wall palette.

Sentinel's existing twin-barrel sprites, Bastion's 96x96 sprites, all block definitions, stats, ammo, sounds and gameplay code are unchanged.

## Validation

python3 tools/check_assets.py checks each block sprite and turret base sprite against size * 32, checks PNG headers, and verifies the required name/description keys in both Russian bundles. It uses only the Python standard library.

Executed fixture checks:
- Valid 1x1, 2x2 and 3x3 sprite sizes plus complete Russian keys: exit 0.
- Deliberately undersized 32x32 Bulwark sprite for a 2x2 block: exit 1 with the exact 64x64 expectation.
- Deliberately removed Bulwark Russian description key: exit 1 with the missing key identified.
- Deliberately removed an ItemTurret base sprite: exit 1 with the missing asset identified.

The new sprite is 64x64 RGBA with 12 opaque colors and no smoothing/antialiasing. The checker and sprite were syntax/header-checked locally. Mindustry v136 was not launched, so atlas rendering and actual in-game appearance are not claimed as tested.

## iPhone acceptance before merge

Import the ZIP for daily/bulwark-sprite-20261112, restart Mindustry and confirm version 0.2-test-bulwark-art-20261112. In a disposable sandbox, place the 1x1 Wall beside the 2x2 Bulwark. Confirm Bulwark artwork fills its full 2x2 footprint, remains centered on tile boundaries, and is visibly heavier without changing the Sentinel's gray body, orange accents or two straight barrels. Save and reload the world, then confirm both wall types retain their artwork and collision footprint. Keep this branch separate from main until the visual check is accepted.
