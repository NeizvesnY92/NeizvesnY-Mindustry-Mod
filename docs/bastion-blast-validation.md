# Bastion blast ammunition — 2026-11-07

Base: 7c80668d88e72d262b78d22556bd8e4013b8ca41 (latest cooling test branch). Fetched current remote branches and reviewed main and test histories, README, tools instructions and content definitions. No AGENTS.md is tracked. Main remains f26dcdef469dcf3fde1890ea33d7dc4abb170236. All prior test changes are preserved; sprites and sounds are unchanged.

One gameplay addition: native BasicBulletType for blast-compound in Bastion. Direct damage 35, splash 35 with native distance falloff, radius 24 (3 tiles), 2 charges/item. Existing magazine 30, range 400, reload 24 and original three ammunition definitions unchanged. No piercing, homing, fire or custom runtime scripts. Updated English/Russian descriptions, test version and general ammunition checker.

Executed the official Mindustry v136 server-release.jar with Java 17:
- check_mod.py passed: content, research parents, ammunition including blast compound, projectile range.
- check_blast.py passed: accepted blast compound, 15 items filled 30 charges, rejected additional ammo when full, selected and consumed the correct bullet, switched to copper after freeing capacity.
- Actual BulletType.hitEntity and hit handlers on engine units: 35 direct damage, 70 total at explosion center, nearby ground and air units damaged, unit 40 units away and allied unit at center untouched. Uses a synthetic world and engine team spatial indices, not an autonomous combat session.
- Negative control omitted the explosion handler call: checker failed on center splash damage (35 instead of 70), exit 1.
- check_pyratite.py and check_cooling.py passed unchanged.
- git diff --check passed. Original ammunition definitions and all sprite/sound files retained from base.

Not verified: live targeting/flight under battle conditions, building explosion damage, visible effects/audio, performance and save/load on iPhone. Native building explosion behavior has not been independently asserted here.

## iPhone check before merge

Import the ZIP of daily/bastion-blast-ammo-20261107 and restart; confirm version 0.2-test-blast-20261107. In a sandbox, feed blast compound to Bastion and compare a tight enemy group with widely separated targets. Check flying targets and long-range shots. Compare with graphite against a single durable target and note whether blast ammo is too strong or weak. Switch between blast compound and copper/graphite/silicon via normal delivery, then save and reload with a partial magazine. Check effects, sound and remaining ammunition. Keep this branch separate from main until reviewed.
