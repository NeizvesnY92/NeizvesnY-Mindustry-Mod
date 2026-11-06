# Sentinel optional cooling — 2026-11-06

Base: e606a58b17a6b1459704dd415b75feaba07ae9e7 (latest pyratite test branch). All local base files matched remote Git blob hashes. No AGENTS.md exists in the remote tree. Read README, tools instructions, block definitions and recent main/test branch history.

Added native v136 ConsumeCoolant at 0.1 units/tick, capacity 20, multiplier 5. Engine makes it optional and a booster. No mandatory liquid requirement. No sprites, bullets, damage, ammo or existing mechanics changed.

Executed official v136 server-release.jar with Java 17:
- check_mod.py: four blocks, research parents, ammunition and range passed.
- check_pyratite.py: burn hit handler, storage and previous improvements passed.
- check_cooling.py: actual updateTile calls on a detached building, delta=1. Dry reload increment 1, water 1.2, cryofluid 1.45. Accepted water/cryofluid; rejected oil/slag. Used 0.1 liquid per cooling tick. No liquid use at full reload. Resumed dry reload when coolant depleted. Ammo unchanged.
- Disposable negative copy with coolant amount 0.2: checker rejected configuration, exit 1.

These are engine checks, not a live combat simulation. iPhone: connect a conduit, compare dry/water/cryofluid firing, disconnect supply and exhaust tank, switch ammunition, then save/reload with coolant and ammo present. Check liquid UI and balance. This build remains separate from main until those checks.
