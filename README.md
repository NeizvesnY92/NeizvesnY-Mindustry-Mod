# NeizvesnY Mindustry Mod

## Blocks

- NeizvesnY Wall: 1x1 armored wall.
- NeizvesnY Bulwark: 2x2 heavy wall, 2100 health, 9 armor.
- NeizvesnY Sentinel: 2x2 fast twin-barrel turret, 320 range.
- NeizvesnY Bastion: 3x3 heavy twin-barrel turret, 400 range.

Both turrets accept copper, graphite, and silicon. Graphite is stronger; silicon boosts fire rate. Sentinel also accepts pyratite; Bastion also accepts blast compound and thorium.

## Install

Import the GitHub repository from Mindustry's Mods menu, or download the ZIP and import it.

## Status

The original Sentinel and wall are player-tested. Bastion uses dedicated 96x96 sprites for its 3x3 footprint. New gameplay changes remain in test branches pending iPhone testing.

## Sentinel optional coolant (test build)

Water and cryofluid speed up Sentinel reload. Dry operation keeps the original reload of 9 ticks. Feed liquid through a conduit. Water adds 20% reload speed, cryofluid 45%; maximum consumption is 6 liquid units/second while cooling. Previous combined improvements and pyratite ammunition are included. Requires iPhone combat and save/load testing before merge.

## Bastion blast compound ammunition (test build)

Feed blast compound to Bastion for explosive shells: 35 direct damage plus up to 35 splash damage (decreases with distance), radius 24 world units / 3 tiles. Hits both air and ground enemies; allies are excluded by the native explosion handler. Each item supplies 2 shots; the existing 30-charge magazine, range 400 and reload 24 ticks remain unchanged. Copper, graphite and silicon retain their existing behavior. Uses native Mindustry effects and the existing pixel sprites.

This branch includes the previous combined improvements, Sentinel pyratite and optional cooling. Run `python3 tools/check_blast.py /absolute/path/to/server-release.jar` for loaded-engine ammunition and explosion checks. Test combat balance, effects, supply/switching and save/load on iPhone before merging.

## Bastion muzzle alignment fix (test build)

Bastion's 96x96 sprite has wider barrel spacing than the old shot pattern. Shot origins and muzzle flashes now align with the two existing barrel tips: `shootX: 0.5625`, `shootY: 10.5`, alternate spread `7.625` world units. No artwork, ammunition, damage, range, reload or sound changes. Previous test-branch features remain included.

Run `python3 tools/check_muzzles.py /absolute/path/to/server-release.jar` to exercise actual shots with all four ammunition types at six rotations. Version `0.2-test-muzzles-20261108` stays in `daily/bastion-shot-origin-20261108` pending an iPhone visual/combat check. See `docs/bastion-muzzles-validation.md`.


## Bastion thorium ammunition (test build)

Thorium rounds deal 60 direct damage and ignore **unit armor**, using native v136 `pierceArmor`. They stop on the first target: no multi-target penetration, splash, homing or fire. Graphite retains its existing two-unit penetration role. One thorium supplies 2 shots; 15 items fill Bastion's unchanged 30-charge magazine. Speed 4.2, lifetime 100, computed range 420, normal reload multiplier 1. Turret range 400 and reload 24 remain unchanged. Thorium tracers use Mindustry's familiar pink thorium palette; all pixel sprites and sounds are preserved.

`daily/bastion-thorium-20261109` / version `0.2-test-thorium-20261109` includes all previous test-branch work, including corrected Bastion muzzle positions. Run `python3 tools/check_thorium.py /absolute/path/to/server-release.jar`. Armor bypass is verified for unit hits; no building-armor or shield bypass is promised. Requires iPhone combat/balance and save/load checks before merge. See `docs/bastion-thorium-validation.md`.


## Bulwark bullet deflection (test build)

Bulwark can now reflect ordinary moving projectiles using the native v136 Wall mechanic, `chanceDeflect: 10`. Probability is `min(1, 10 / incoming bullet damage)`: for example, 50% at 20 damage and 10% at 100 damage under default damage rules. Bullets moving at 0.1 world units/tick or less and types marked unreflectable are excluded. A reflected bullet changes to the wall's team and reverses one velocity component; the wall still takes its normal collision damage. This does not grant immunity to bullets or general laser reflection.

The extra construction cost is **8 phase fabric**. Existing copper/lead/graphite/plastanium requirements, 2100 health, 9 armor, lightning insulation and compatible-laser absorption remain unchanged. All artwork, sounds and other blocks are preserved. Version `0.2-test-deflection-20261110` in `daily/bulwark-deflection-20261110` includes all preceding test-branch work. Run `python3 tools/check_deflection.py /absolute/path/to/server-release.jar`; see `docs/bulwark-deflection-validation.md`. Keep separate from main until iPhone combat, cost/balance and save/load testing.


## Sentinel graphite impact (test build)

Graphite rounds now apply a small native knockback impulse: `knockback: 0.3`, `impact: true`. Impact directs the impulse along bullet flight rather than the separation vector at contact; unit mass reduces the resulting velocity change. This is intended to help against advancing light units, not to immobilize enemies. Damage 18, speed 4.2, lifetime 80, ammo multiplier 2, range, reload and other ammunition are unchanged. Building targets receive no unit impulse. All pixel sprites and sounds are preserved.

Version `0.2-test-impact-20261111` in `daily/sentinel-graphite-impact-20261111` includes all preceding test-branch work. Run `python3 tools/check_impact.py /absolute/path/to/server-release.jar`; see `docs/sentinel-impact-validation.md`. Requires iPhone combat/balance, effects and save/load testing before merge.
