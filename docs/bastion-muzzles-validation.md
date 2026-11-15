# Bastion muzzle alignment — 2026-11-08

Base: `69160fa6fa0ac501f086d1a3203fc33ec9be23ee`, current remote `daily/bastion-blast-ammo-20261107`. Fetched all remote refs, read main and test histories, README, tools instructions, content and validation notes. Main is still `f26dcdef469dcf3fde1890ea33d7dc4abb170236`. No tracked AGENTS.md or local ancestor instructions were found. New work uses a separate worktree; existing untracked Python caches and other checkouts are untouched.

## Reproduced defect and fix

The Bastion sprite was enlarged to 96x96 in `0d588a7`, but `ShootAlternate.spread` remained 5 world units and `shootY` retained the size-derived default 12. The image uses 4 pixels/world unit. At the top edge, y=6, opaque barrel intervals are x=[27,43) and [57,74); centers are 35 and 65.5. Relative to texture origin (48,48), the two muzzle positions are (-3.25,10.5) and (4.375,10.5).

Set `shootX=0.5625`, `shootY=10.5` and alternate `spread=7.625` to match those centers. The small horizontal offset accounts for the existing sprite's asymmetric raster placement. The old origins were (-2.5,12) and (2.5,12), too close together and ahead of the tips. Native Turret uses the same coordinates for projectiles, shoot effects and smoke effects. This corrects shot origin geometry without changing any PNGs. Sentinel remains untouched.

Engine references: [v136 Turret.java](https://github.com/Anuken/Mindustry/blob/v136/core/src/mindustry/world/blocks/defense/turrets/Turret.java), [v136 ShootAlternate.java](https://github.com/Anuken/Mindustry/blob/v136/core/src/mindustry/entities/pattern/ShootAlternate.java). No runtime scripts or new engine APIs are shipped.

## Executed validation

Official v136 server-release.jar, downloaded from the official release URL; embedded version.properties reports `build=136`, `type=official`. SHA256: `67700395c408d12703ee6ebd26fe3d75c81dbcb1c2a1cdbaa48654da1c7e7067`. Runtime: OpenJDK 17.0.20.

- Before changing HJSON, the new check failed on an actual copper shot: expected approximately (266.5,259.25), actual (268,258.5) at rotation 0, exit 1. The loaded original fields were shootX=0, shootY=12, spread=5.
- After the fix, `check_muzzles.py` passed 48 actual shots via `updateTile`: both consecutive alternating barrels at 0,45,90,180,225,270 degrees, for copper, graphite, silicon and blast compound. The check compensates for native BulletType.create backdating by velocity*delta; compares launch positions, bullet type, shot count and ammunition consumption.
- Existing `check_mod.py`, `check_blast.py`, `check_cooling.py` and `check_pyratite.py` all passed, exit 0.
- `git diff --check` passed. All sprite/sound bytes and all block definitions except Bastion's three shot-origin parameters are unchanged from base. Damage, ammo, targeting range and firing interval are unchanged.

These are headless engine checks with detached turret buildings, not a rendered battle. No iPhone session, visual effect/recoil check, audio check or save/load test was performed. The existing test-branch gameplay remains unapproved for main.

## iPhone acceptance before merge

Import the ZIP of `daily/bastion-shot-origin-20261108`, restart and confirm version `0.2-test-muzzles-20261108`. In a disposable sandbox, fire Bastion with all four ammunition types and rotate/aim in several directions. Check that bullets, flashes and smoke alternate from the two barrel tips, including during sustained recoil. Check near and far targets, then save and reload with a partially filled magazine. Existing pixel art, sound and Sentinel behavior should remain the same. Keep separate from main until the visual/combat result is accepted.
