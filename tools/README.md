# Headless content check

Requires Python 3 and Java compatible with the official Mindustry v136 server JAR. Download server-release.jar from https://github.com/Anuken/Mindustry/releases/tag/v136 separately. The checker does not download or install anything.

From the repository root:

```sh
python3 tools/check_mod.py /absolute/path/to/server-release.jar
```

To check another checkout:

```sh
python3 tools/check_mod.py /absolute/path/to/server-release.jar --mod /absolute/path/to/mod
```

The server runs in a temporary directory with a copied mod. Existing game configuration and saves are not used. Exit code 0 requires a successful runtime check; exit code 1 indicates failure or timeout (60 seconds). The checker verifies all four existing blocks, a research parent for each, all three turret ammunition types, and computed bullet range against turret targeting range. Checks use the actual loaded engine objects, not a second HJSON parser.

Validated on 2026-10-31 with official v136: current main passed; a copy with Sentinel copper lifetime reduced to 1 failed for insufficient range; a copy with a nonexistent research parent failed for missing research attachment. These negative tests are disposable mutations, not shipped gameplay changes.

This is a content smoke test, not a combat simulation. It does not prove research parent identity, moving-target hit rate, audio, graphics or iPhone compatibility. Future new blocks and ammunition must be added to CHECK in check_mod.py. The script copies the data asset directories and optional scripts directory. JavaScript is executed by the server in the disposable test copy. Use this checker only with trusted mod code: a temporary working directory is not a security sandbox. Other runtime files must be added to the copy list if introduced.

Regression validation (2026-11-02, official v136): a disposable mod copy containing scripts/main.js with `throw new Error("SCRIPT_REGRESSION_SENTINEL");` incorrectly passed the previous checker because scripts were omitted. With scripts copied, the server reports the JavaScript error and the checker exits 1, even though the content marker still says MOD_CHECK_PASS. The unchanged data-only mod still exits 0. No failing script is installed in the real mod.

## Bastion muzzle regression

```sh
python3 tools/check_muzzles.py /absolute/path/to/server-release.jar
```

Exercises the actual `TurretBuild.updateTile` shooting path: five ammunition types, six orientations and two consecutive alternating barrels (60 bullets). Compares spawn origins with the barrel centers measured from the unchanged 96x96 Bastion sprite, accounts for native bullet backdating, and checks one charge consumed per shot. No extra Python dependencies. Geometry expectations must be reviewed if the sprite changes. This does not render muzzle flashes, recoil, sound or iPhone graphics.


## Bastion thorium ammunition

```sh
python3 tools/check_thorium.py /absolute/path/to/server-release.jar
```

Checks native ammo acceptance, full capacity, consumption, switching, mixed-ammo state serialization, damage against synthetic ground/air units with 0 and 30 armor, a graphite control, and removal after one actual unit collision. Uses an existing official v136 server JAR. Serialization uses the building's native write/read methods in memory; it is not a full world save/load or an iPhone test.
