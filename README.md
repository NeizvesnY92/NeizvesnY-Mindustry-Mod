# NeizvesnY Mindustry Mod

## Blocks

- NeizvesnY Wall: 1x1 armored wall.
- NeizvesnY Bulwark: 2x2 heavy wall, 2100 health, 9 armor.
- NeizvesnY Sentinel: 2x2 fast twin-barrel turret, 320 range.
- NeizvesnY Bastion: 3x3 heavy twin-barrel turret, 400 range.

Both turrets accept copper, graphite, and silicon. Graphite is stronger; silicon boosts fire rate. Sentinel also accepts pyratite; Bastion also accepts blast compound.

## Install

Import the GitHub repository from Mindustry's Mods menu, or download the ZIP and import it.

## Status

The original Sentinel and wall are player-tested. Bastion uses dedicated 96x96 sprites for its 3x3 footprint. New gameplay changes remain in test branches pending iPhone testing.

## Sentinel optional coolant (test build)

Water and cryofluid speed up Sentinel reload. Dry operation keeps the original reload of 9 ticks. Feed liquid through a conduit. Water adds 20% reload speed, cryofluid 45%; maximum consumption is 6 liquid units/second while cooling. Previous combined improvements and pyratite ammunition are included. Requires iPhone combat and save/load testing before merge.

## Bastion blast compound ammunition (test build)

Feed blast compound to Bastion for explosive shells: 35 direct damage plus up to 35 splash damage (decreases with distance), radius 24 world units / 3 tiles. Hits both air and ground enemies; allies are excluded by the native explosion handler. Each item supplies 2 shots; the existing 30-charge magazine, range 400 and reload 24 ticks remain unchanged. Copper, graphite and silicon retain their existing behavior. Uses native Mindustry effects and the existing pixel sprites.

This branch includes the previous combined improvements, Sentinel pyratite and optional cooling. Run `python3 tools/check_blast.py /absolute/path/to/server-release.jar` for loaded-engine ammunition and explosion checks. Test combat balance, effects, supply/switching and save/load on iPhone before merging.
