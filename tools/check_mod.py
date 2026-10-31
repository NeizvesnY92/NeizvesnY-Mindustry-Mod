#!/usr/bin/env python3
"""Check loaded mod content using an existing official Mindustry server JAR."""
import argparse
from pathlib import Path
import re
import shutil
import subprocess
import tempfile

CHECK = r'''
try {
  var prefix = "neizvesny-mindustry-mod-";
  var names = ["neizvesny-wall", "neizvesny-bulwark", "neizvesny-sentinel", "neizvesny-bastion"];
  for (var i = 0; i < names.length; i++) {
    var block = Vars.content.block(prefix + names[i]);
    if (block == null) throw new Error("Missing block: " + names[i]);
    var found = false;
    for (var n = 0; n < TechTree.all.size; n++) {
      var node = TechTree.all.get(n);
      if (node.content == block && node.parent != null) found = true;
    }
    if (!found) throw new Error("Missing research parent: " + names[i]);
    if (block instanceof ItemTurret) {
      var items = [Items.copper, Items.graphite, Items.silicon];
      for (var j = 0; j < items.length; j++) {
        var bullet = block.ammoTypes.get(items[j]);
        if (bullet == null) throw new Error("Missing ammo: " + names[i] + "/" + items[j].name);
        if (bullet.range + 0.01 < block.range + bullet.rangeChange)
          throw new Error("Insufficient ammo range: " + names[i] + "/" + items[j].name);
      }
    }
  }
  print("MOD_CHECK_PASS");
} catch (error) { print("MOD_CHECK_FAIL: " + error); }
'''


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("server_jar", type=Path)
    parser.add_argument("--mod", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    jar = args.server_jar.resolve(strict=True)
    source = args.mod.resolve(strict=True)
    if not (source / "mod.hjson").is_file():
        parser.error("--mod must contain mod.hjson")
    with tempfile.TemporaryDirectory(prefix="mindustry-check-") as work:
        target = Path(work) / "config/mods/neizvesny"
        target.mkdir(parents=True)
        for name in ("mod.hjson", "content", "bundles", "sprites", "sounds"):
            src = source / name
            if src.is_dir():
                shutil.copytree(src, target / name)
            elif src.is_file():
                shutil.copy2(src, target / name)
        commands = "js " + " ".join(CHECK.splitlines()) + "\nexit\n"
        try:
            result = subprocess.run(["java", "-jar", str(jar)], input=commands,
                                    text=True, stdout=subprocess.PIPE,
                                    stderr=subprocess.STDOUT, cwd=work, timeout=60)
        except subprocess.TimeoutExpired:
            print("FAIL: headless check timed out")
            return 1
        output = re.sub(r"\x1b\[[0-9;]*m", "", result.stdout)
        print(output, end="")
        return int(result.returncode != 0 or "MOD_CHECK_PASS" not in output
                   or "MOD_CHECK_FAIL" in output or "[E]" in output)


if __name__ == "__main__":
    raise SystemExit(main())
