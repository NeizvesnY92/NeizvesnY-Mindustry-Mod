# Sentinel pyratite test — 2026-11-05

Based on test/combined-20261102 at 0d588a7. Keeps Bastion 96x96 art, heavy rounds, Bulwark insulation, Sentinel silicon homing and 60-charge magazine. Incorporates the latest main content checker (exact research parents and required turret types).

Sentinel accepts pyratite: 14 direct damage, speed 3.5, lifetime 100, two charges per item, burning for 180 ticks (3 seconds at normal speed). No splash, homing, fire puddles or reload bonus on this ammunition. Burning applies to susceptible units, not buildings or immune units. Existing ammunition and artwork are unchanged.

Official Mindustry v136 headless checks:

- `python3 tools/check_mod.py /path/to/server-release.jar`: all four blocks, research parents, turret types and ammunition reach.
- `python3 tools/check_pyratite.py /path/to/server-release.jar`: loaded bullet fields, retained magazine/homing, acceptance and capacity (30 pyratite = 60 charges), direct hitEntity call on a Dagger applies 180 ticks of burning.
- Disposable copy with status changed to none is rejected by the pyratite check.

These checks do not run a battle or render effects. On iPhone import this branch ZIP, restart, verify version 0.2-test-pyratite-20261105. In sandbox supply Sentinel with pyratite and compare with copper against ordinary moving ground units. Check ignition, practical damage, switching back to other ammo, full magazine and save/reload. Balance and visible effects need player testing before merging into main.
