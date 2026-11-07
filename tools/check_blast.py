#!/usr/bin/env python3
"""Exercise Bastion blast ammunition with the loaded v136 hit handler."""
import check_mod

check_mod.CHECK = r'''
try {
 var block=Vars.content.block("neizvesny-mindustry-mod-neizvesny-bastion");
 var type=block.ammoTypes.get(Items.blastCompound);
 if(type == null) throw new Error("missing blast compound ammunition");
 if(type.damage != 35 || type.splashDamage != 35 || type.splashDamageRadius != 24) throw new Error("wrong explosion stats");
 if(type.range < block.range || type.ammoMultiplier != 2 || type.pierce) throw new Error("wrong range, multiplier or piercing");
 if(!type.collidesAir || !type.collidesGround || type.collidesTeam) throw new Error("wrong target filters");
 var build=block.newBuilding().create(block,Team.sharded);
 if(!build.acceptItem(null,Items.blastCompound)) throw new Error("blast ammo rejected");
 build.handleStack(Items.blastCompound,15,null);
 if(build.totalAmmo != 30 || build.acceptItem(null,Items.blastCompound)) throw new Error("ammo capacity");
 if(build.peekAmmo() != type || build.useAmmo() != type || build.totalAmmo != 29) throw new Error("ammo selection or use");
 build.useAmmo();
 if(!build.acceptItem(null,Items.copper)) throw new Error("copper rejected after freeing capacity");
 build.handleItem(null,Items.copper);
 if(build.peekAmmo() != block.ammoTypes.get(Items.copper)) throw new Error("ammo switching");
 Vars.world.resize(64,64);
 function target(unitType,team,x,y) {
   var u=unitType.create(team); u.set(x,y); u.add(); return u;
 }
 var direct=target(UnitTypes.dagger,Team.crux,128,128);
 var nearby=target(UnitTypes.dagger,Team.crux,140,128);
 var air=target(UnitTypes.flare,Team.crux,128,140);
 var outside=target(UnitTypes.dagger,Team.crux,168,128);
 var friendly=target(UnitTypes.dagger,Team.sharded,128,128);
 Vars.state.teams.updateTeamStats();
 var hd=direct.health, hn=nearby.health, ha=air.health, ho=outside.health, hf=friendly.health;
 var bullet=Bullet.create(); bullet.type=type; bullet.damage=type.damage; bullet.team=Team.sharded;
 type.hitEntity(bullet,direct,direct.health);
 if(Math.abs(hd-direct.health-35)>0.001) throw new Error("direct damage");
 type.hit(bullet,128,128);
 if(Math.abs(hd-direct.health-70)>0.001) throw new Error("center splash damage: "+(hd-direct.health));
 if(!(nearby.health < hn && air.health < ha)) throw new Error("splash missed nearby ground or air target");
 if(outside.health != ho || friendly.health != hf) throw new Error("splash damaged outside radius or ally");
 print("MOD_CHECK_PASS: blast loading, capacity, use, switching, direct and splash damage, air/ground, radius and allies verified");
} catch(error) { print("MOD_CHECK_FAIL: "+error); }
'''

if __name__ == "__main__":
    raise SystemExit(check_mod.main())
