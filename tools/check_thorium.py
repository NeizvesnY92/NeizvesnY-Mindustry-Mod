#!/usr/bin/env python3
"""Exercise Bastion thorium ammo and unit armor handling on Mindustry v136."""
import check_mod

check_mod.CHECK = r'''
try {
 var block=Vars.content.block("neizvesny-mindustry-mod-neizvesny-bastion");
 var type=block.ammoTypes.get(Items.thorium);
 var graphite=block.ammoTypes.get(Items.graphite);
 if(type==null) throw new Error("missing thorium ammo");
 if(type.damage!=60 || type.range<block.range || type.ammoMultiplier!=2 || type.reloadMultiplier!=1)
   throw new Error("wrong damage, range or ammo economy");
 if(type.pierce || type.pierceBuilding || type.splashDamage!=0 || type.homingPower!=0)
   throw new Error("unexpected penetration, splash or homing");
 if(!type.collidesAir || !type.collidesGround || type.collidesTeam) throw new Error("wrong target filters");
 var build=block.newBuilding().create(block,Team.sharded);
 if(!build.acceptItem(null,Items.thorium)) throw new Error("thorium rejected");
 build.handleStack(Items.thorium,15,null);
 if(build.totalAmmo!=30 || build.acceptItem(null,Items.thorium)) throw new Error("wrong capacity");
 if(build.useAmmo()!=type || build.totalAmmo!=29) throw new Error("wrong ammo use");
 build.useAmmo(); build.useAmmo(); build.useAmmo();
 if(!build.acceptItem(null,Items.copper)) throw new Error("copper rejected after freeing capacity");
 build.handleItem(null,Items.copper);
 if(build.peekAmmo()!=block.ammoTypes.get(Items.copper)) throw new Error("switching to copper failed");
 if(!build.acceptItem(null,Items.thorium)) throw new Error("thorium rejected during switching");
 build.handleItem(null,Items.thorium);
 if(build.peekAmmo()!=type) throw new Error("switching back to thorium failed");
 build.reloadCounter=12; build.rotation=37;
 var out=new java.io.ByteArrayOutputStream();
 build.write(Writes.get(new java.io.DataOutputStream(out)));
 var restored=block.newBuilding().create(block,Team.sharded);
 restored.read(Reads.get(new java.io.DataInputStream(new java.io.ByteArrayInputStream(out.toByteArray()))),build.version());
 if(restored.totalAmmo!=30 || restored.ammo.size!=2 || restored.peekAmmo()!=type
    || restored.reloadCounter!=12 || restored.rotation!=37) throw new Error("ammo state serialization failed");
 for(var s=0;s<28;s++) if(restored.useAmmo()!=type) throw new Error("restored thorium quantity incorrect");
 if(restored.totalAmmo!=2 || restored.peekAmmo()!=block.ammoTypes.get(Items.copper)) throw new Error("restored copper stack lost");
 Vars.world.resize(64,64);
 function target(unitType,armor) {
   var u=unitType.create(Team.crux); u.set(128,128); u.armor=armor;
   u.maxHealth=1000; u.health=1000; u.add(); return u;
 }
 function hit(bulletType,unit) {
   var b=Bullet.create(); b.type=bulletType; b.damage=bulletType.damage; b.team=Team.sharded;
   var before=unit.health; bulletType.hitEntity(b,unit,before); return before-unit.health;
 }
 var unitTypes=[UnitTypes.dagger,UnitTypes.flare];
 for(var i=0;i<unitTypes.length;i++) {
   var plain=target(unitTypes[i],0), armored=target(unitTypes[i],30), control=target(unitTypes[i],30);
   var normalDamage=hit(type,plain), armorDamage=hit(type,armored), graphiteDamage=hit(graphite,control);
   if(Math.abs(normalDamage-60)>0.001 || Math.abs(armorDamage-60)>0.001)
     throw new Error("thorium armor bypass failed: "+unitTypes[i].name+" plain="+normalDamage+" armored="+armorDamage);
   if(Math.abs(graphiteDamage-30)>0.001) throw new Error("graphite control did not respect armor: "+graphiteDamage);
 }
 var victim=target(UnitTypes.dagger,30);
 var bullet=type.create(build,Team.sharded,128,128,0);
 bullet.collision(victim,128,128);
 if(Math.abs(victim.health-940)>0.001 || bullet.isAdded()) throw new Error("thorium did not stop after first unit hit");
 print("MOD_CHECK_PASS: thorium capacity, use, switching, mixed-ammo serialization, ground/air armor bypass, graphite control and first-hit removal verified");
} catch(error) { print("MOD_CHECK_FAIL: "+error); }
'''

if __name__ == "__main__":
    raise SystemExit(check_mod.main())
