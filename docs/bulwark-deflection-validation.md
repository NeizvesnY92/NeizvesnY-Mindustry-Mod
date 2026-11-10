# Bulwark bullet deflection — 2026-11-10

Base: `0de67006f380b7aa4ad4967f2a8f71e6e7091c79`, latest remote thorium test branch. Fetched all refs and reviewed current main/test histories, README, tools instructions and block definitions. No tracked or ancestor AGENTS.md was found. Main remains `f26dcdef469dcf3fde1890ea33d7dc4abb170236`. No repeated feature was found in history. Work uses a separate worktree and preserves existing user checkouts/files.

## Change

Added native `chanceDeflect: 10` to Bulwark, with 8 phase fabric added to construction cost. Existing material quantities, health=2100, armor=9, size=2, insulation and compatible-laser absorption stay unchanged. Existing sprites and sounds are unchanged; no runtime scripts added. Both Russian bundles and the English description explain the mechanic and extra cost.

Native v136 probability is chanceDeflect / bullet.damage(), capped by the chance operation: 50% at 20 damage, 10% at 100 damage with default damage multipliers. Slow projectiles (speed <=0.1) and unreflectable types are excluded. Reflection changes bullet team/owner, reverses the appropriate velocity component and extends its life by one tick. The wall takes normal damage before attempting reflection. Does not promise immunity, reflection of beams or protected-projectile reflection.

Reference: [official v136 Wall.java](https://github.com/Anuken/Mindustry/blob/v136/core/src/mindustry/world/blocks/defense/Wall.java), WallBuild.collision. New material cost and defensive strength are experimental pending playtesting.

## Executed validation

Official Mindustry v136 server-release.jar, embedded version.properties build=136/type=official; SHA256 `67700395c408d12703ee6ebd26fe3d75c81dbcb1c2a1cdbaa48654da1c7e7067`. OpenJDK 21.0.13.

- `check_deflection.py` places a real Bulwark building into a synthetic tiled world and calls native WallBuild.collision. A 5-damage moving reflectable bullet returned false (not absorbed), changed to the wall's team and owner, reversed X velocity and damaged the wall.
- Reflected bullet's native collision filters accepted an enemy Dagger and rejected an allied Dagger. Its actual unit collision dealt 5 damage and removed the bullet.
- Unreflectable and speed=0.05 bullets were not reflected and retained their enemy team.
- 100 synthetic 100-damage impacts with seed 12345 produced 5 reflections and 95 normal stops. This is one deterministic test sample, not an estimate of the theoretical 10% probability.
- Cost includes phase fabric/8. Existing insulation/laser absorption flags, health/armor and unchanged small-wall stats were asserted.
- Negative control disables chanceDeflect on the loaded engine object after initial field assertions: test rejected the missing actual reflection.
- All existing checks passed: check_mod, check_blast, check_cooling, check_pyratite, check_muzzles (60 actual shots), check_thorium. Parallel Java processes printed harmless shared perf-data lock warnings; all checks completed with exit 0.
- `git diff --check` passed. Other block definitions, old material quantities, all sprites and sounds were compared with the base and retained unchanged.

No autonomous battle, graphics/audio session, full world save/load or iPhone test was performed. Prior experimental mechanics remain separate from main. Insulation/laser absorption were retained and checked as flags, not re-simulated here.

## iPhone checks before merge

Import `daily/bulwark-deflection-20261110`, restart and confirm `0.2-test-deflection-20261110`. In a disposable sandbox, build Bulwark with the added phase fabric cost. Face ordinary enemy gunfire: some bullets should bounce toward enemies while the wall still loses health. Compare light and heavy fire and judge whether the resource cost is fair. Check construction/reconstruction and existing laser/lightning protection. Save/reload a damaged wall and repeat the test. Confirm unchanged pixel art and previous turret behavior. Merge only after combat and cost/balance are accepted.
