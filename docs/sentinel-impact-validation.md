# Sentinel graphite impact — 2026-11-11

Base: `237c24e9b7116ec6aef6d06be62136c1ab2dd400`, latest remote Bulwark deflection test branch. Fetched current refs, read main/test history, all block definitions, README and tools instructions. No tracked or ancestor AGENTS.md was found. Main remains `f26dcdef469dcf3fde1890ea33d7dc4abb170236`. This mechanic was not present in history. A separate worktree preserves other checkouts and user files.

## Change

Added `knockback: 0.3` and `impact: true` only to Sentinel graphite rounds. Native v136 hitEntity applies a magnitude-24 impulse along bullet flight; the unit's impulse handler scales velocity by inverse mass. The intended role is mild disruption of advancing light units, without a new ammunition type or more direct damage. This is experimental balance, not player-approved crowd control.

All old damage/speed/lifetime/range/reload/ammo values, all other ammo, all other blocks, pixel sprites and sounds are preserved. English and both Russian descriptions mention the impulse. No runtime scripts or new engine APIs are shipped.

Reference: [official v136 BulletType.java](https://github.com/Anuken/Mindustry/blob/v136/core/src/mindustry/entities/bullet/BulletType.java), hitEntity: knockback*80, impact direction from bullet.rotation, unit.impulse. Buildings are not Unit instances and receive no such impulse.

## Executed checks

Official v136 server-release.jar: embedded build=136/type=official, SHA256 `67700395c408d12703ee6ebd26fe3d75c81dbcb1c2a1cdbaa48654da1c7e7067`. Runtime OpenJDK 21.0.13.

- `check_impact.py` invoked the actual native hit handler for Dagger, Fortress and Flare at 0,90,180,270 degrees (12 combinations). Units had zero assigned armor/velocity to isolate damage and impulse. Off-axis bullet placement distinguishes flight-directed impact from radial separation.
- Damage stayed 18. Velocity components matched magnitude 24/unit.mass() in the expected direction. Dagger velocity change was approximately 0.119366, Fortress 0.045204 world units/tick. This is an instantaneous change, not lasting displacement or net movement in battle.
- One actual graphite projectile collision applied the expected damage and velocity change and removed the non-piercing projectile.
- Copper, silicon and pyratite controls gave zero knockback; 30 graphite still fill 60 charges and firing consumes one charge.
- Disposable negative copies with knockback=0 and impact=false each failed on actual velocity/direction assertions, exit 1.
- All seven existing checks passed: check_mod, check_blast, check_cooling, check_pyratite, check_muzzles (60 Bastion shots), check_thorium and check_deflection. Parallel JVM perf-data lock warnings did not prevent checks; all completed with exit 0.
- `git diff --check` passed. Compared preserved block fields and sprite/sound bytes against base.

These are synthetic engine tests, not an autonomous battle. They do not establish practical crowd control, moving-target hit rate, balance, visuals/audio or iPhone behavior. Full-world save/load was not run.

## iPhone checks before merge

Import `daily/sentinel-graphite-impact-20261111`, restart and confirm `0.2-test-impact-20261111`. In a disposable sandbox compare graphite with copper against advancing light ground units, then heavier units and air targets. Check for a small push along bullet flight, no accidental pull toward the turret, and acceptable movement under sustained fire. Check dry and cooled firing, unchanged artwork/sound and normal ammo switching. Save/reload with graphite and coolant in the turret. Keep separate from main until combat and balance are accepted.
