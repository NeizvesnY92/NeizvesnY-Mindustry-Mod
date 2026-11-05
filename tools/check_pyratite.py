#!/usr/bin/env python3
"""Run isolated v136 pyratite loading, storage and hit-handler checks."""
import check_mod

check_mod.CHECK=r'''
try {
 var block=Vars.content.block("neizvesny-mindustry-mod-neizvesny-sentinel");
 var type=block.ammoTypes.get(Items.pyratite);
 if(type == null) throw new Error("missing pyratite");
 if(type.status != StatusEffects.burning || type.statusDuration != 180) throw new Error("wrong burn");
 if(type.damage != 14 || type.range < block.range || type.ammoMultiplier != 2) throw new Error("wrong bullet stats");
 if(block.maxAmmo != 60 || Math.abs(block.ammoTypes.get(Items.silicon).homingPower - 0.04) > 0.00001) throw new Error("lost combined improvements");
 var build=block.newBuilding().create(block,Team.sharded);
 if(!build.acceptItem(null,Items.pyratite)) throw new Error("ammo rejected");
 build.handleStack(Items.pyratite,30,null);
 if(build.totalAmmo != 60 || build.acceptItem(null,Items.pyratite)) throw new Error("capacity");
 if(build.peekAmmo() != type) throw new Error("wrong selected bullet");
 var unit=UnitTypes.dagger.create(Team.crux);
 var bullet=Bullet.create(); bullet.type=type; bullet.damage=type.damage; bullet.team=Team.sharded;
 type.hitEntity(bullet,unit,unit.health);
 if(unit.getDuration(StatusEffects.burning) != 180) throw new Error("hit did not apply burn");
 print("MOD_CHECK_PASS: pyratite accepted, 30 items = 60 charges, hit applies burning");
} catch(error) { print("MOD_CHECK_FAIL: "+error); }
'''

if __name__ == "__main__":
    raise SystemExit(check_mod.main())
