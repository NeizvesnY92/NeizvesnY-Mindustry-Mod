# Bastion thorium ammunition — 2026-11-09

Base: `c4770c9662a91c4dd6af1a2875d42df12a8598ae`, current remote `daily/bastion-shot-origin-20261108`. Fetched current refs and reviewed main/test histories, current README, tools instructions and content. No tracked or ancestor AGENTS.md was found. Main remains `f26dcdef469dcf3fde1890ea33d7dc4abb170236`. Used a new worktree; existing user files and other checkouts are untouched.

## Change and role

Added native BasicBulletType for Bastion's thorium ammunition: 60 direct damage, `pierceArmor: true`, 2 charges/item, speed 4.2, lifetime 100 (420 computed range). No splash, homing, fire or penetration through multiple targets/buildings. Against unarmored targets its direct damage matches graphite; graphite keeps its two-unit penetration advantage. Thorium is intended for armored single units at a higher resource cost. This is an experimental balance, not player-approved balance.

Only native v136 fields are used, with no runtime scripts. Reference: [v136 BulletType.hitEntity](https://github.com/Anuken/Mindustry/blob/v136/core/src/mindustry/entities/bullet/BulletType.java) selects `damagePierce` for pierceArmor, otherwise `damage`. This change promises unit-armor bypass only, not shield or building-armor bypass. Added descriptions in English and both Russian bundles, test version and ammunition checks. Existing block settings and all art/audio are preserved.

## Executed checks

Official Mindustry v136 server-release.jar from the official release, embedded build=136, type=official. SHA256 `67700395c408d12703ee6ebd26fe3d75c81dbcb1c2a1cdbaa48654da1c7e7067`, OpenJDK 17.

- `check_thorium.py`: 15 thorium fill 30 charges; full magazine rejects more; each shot consumes one charge; accepted copper and switched back to thorium after freeing capacity.
- Native building write/read round-trip in memory preserved two ammo stacks (28 thorium charges, 2 copper charges), selected ammo, reload progress and rotation. Consuming restored thorium revealed the preserved copper stack.
- Actual hitEntity handler against Dagger and Flare instances, each tested at 0 and 30 assigned armor: thorium dealt 60 in all cases. Graphite control dealt 30 against armor 30. These are synthetic unit instances, not an autonomous battle.
- Actual Bullet.collision removed the thorium bullet after one armored unit hit and dealt 60 damage.
- Disposable negative copy with pierceArmor=false was rejected on actual damage, not just a field check.
- `check_mod.py`, `check_blast.py`, `check_cooling.py`, `check_pyratite.py` passed. Extended `check_muzzles.py` passed 60 actual shots: five ammunition types, six rotations, both alternating barrels, correct origin and charge consumption.
- `git diff --check` passed. All pre-existing ammunition definitions, all other blocks, sprite files and sounds were compared against the base and retained unchanged.

Not verified: rendered combat/flight, moving-target hit rate, effects/audio, live supply, balance, full-world saves or iPhone behavior. Native in-memory serialization is not a substitute for a complete game save/load.

## iPhone check before merge

Import `daily/bastion-thorium-20261109`, restart and confirm `0.2-test-thorium-20261109`. In a disposable sandbox feed thorium to Bastion. Compare it with graphite against armored ground and air units, and against a line of two targets: thorium should stop at the first. Check normal delivery, switching to other ammo, pink tracers and alternating barrel effects. Test near maximum range. Save/reload with a partially filled mixed magazine. Judge whether the armor advantage is worth the thorium cost. Keep this branch separate from main until those checks are accepted.
