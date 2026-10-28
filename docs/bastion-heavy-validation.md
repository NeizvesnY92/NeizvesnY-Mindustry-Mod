# Bastion heavy-role experiment

Sentinel and all artwork remain unchanged. Bastion retains 400 range and its existing cost, but reload changes from 14 to 24 ticks and inaccuracy from 3 to 1 degrees. Copper damage is 40, graphite 60, silicon 45. Graphite pierces at most two units; buildings still stop it. Silicon retains 1.35 reload multiplier.

At 60 ticks/sec, direct single-target DPS before armor: copper 100, graphite 150, silicon 151.875. Sentinel: 80, 120, 135 respectively. Bastion trades tracking speed, footprint and cost for reach, accuracy, stronger individual hits and limited crowd penetration. This is an experimental starting balance, not player-tested balance.

Compatibility reference: Anuken/Mindustry v136 core/src/mindustry/entities/bullet/BulletType.java (pierce, pierceCap, reloadMultiplier) and entities/pattern/ShootAlternate.java. No new engine fields are required.

Validation on 2026-10-28: official v136 server-release.jar started with the modified mod installed in config/mods; output reported 1 mods loaded, listed NeizvesnY Mindustry Mod 0.1, and exited normally without content loading errors. Projectile travel remains 437.5 / 420 / 420 world units, above 400 targeting range. Headless does not validate artwork, audio or iPhone behavior.

## iPhone check

Download this branch as ZIP from GitHub and import via Mods > Import mod, with the existing copy disabled/removed after backing up saves. Restart. In sandbox, supply each turret with each ammo separately; compare firing interval, maximum-range hits and air targeting. Put two enemy ground units in line: graphite should pass through the first and stop after the second, while copper and silicon stop on first hit. Confirm buildings stop graphite. Check alternating barrel flashes, unchanged Sentinel artwork and sound. Use a disposable sandbox save.
