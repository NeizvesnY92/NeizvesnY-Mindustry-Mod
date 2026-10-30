# Sentinel silicon guidance — 2026-10-30

Silicon rounds now use homingPower 0.04, homingRange 50 and homingDelay 8 ticks. In v136 this caps steering at 2 degrees per tick at normal delta; guidance starts after about 0.133 seconds. It is mild trajectory correction, not guaranteed hits. Target selection follows vanilla BulletType.updateHoming; its search center can be the original aim position.

Damage 15, speed 4, lifetime 84, ammo multiplier 2 and reload multiplier 1.35 are unchanged. Copper and graphite remain unguided. Sentinel range remains 320, reload 9. All artwork and sounds are unchanged. Existing Bastion and Bulwark experiment branches are not merged here.

References: Anuken/Mindustry v136 core/src/mindustry/entities/bullet/BulletType.java, fields homingPower/homingRange/homingDelay and updateHoming.

Validation: official v136 server-release.jar loaded the modified mod without content errors. Console inspection returned homingPower approximately 0.04, homingRange 50, homingDelay 8, damage 15 and bullet range 336. Runtime assertions checked copper and graphite homingPower=0, turret reload=9 and range=320. This verifies loading and parameters, not combat performance, visuals, audio or iOS.

On iPhone: back up saves, import this branch ZIP in place of the existing copy and restart. In a disposable sandbox, feed Sentinel silicon and compare its trajectory against moving air and ground targets with copper and graphite. Test near the 320 range limit and against clustered enemies. Confirm the original two-barrel appearance and sound. Do not merge until steering strength and hit rate feel appropriate.
