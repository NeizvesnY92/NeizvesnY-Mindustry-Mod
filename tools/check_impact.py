#!/usr/bin/env python3
"""Exercise Sentinel graphite knockback via the native v136 hit handler."""
import check_mod

check_mod.CHECK = r'''
try {
 var block=Vars.content.block("neizvesny-mindustry-mod-neizvesny-sentinel");
 var type=block.ammoTypes.get(Items.graphite);
 if(type.damage!=18 || Math.abs(type.speed-4.2)>0.00001 || type.lifetime!=80 || type.ammoMultiplier!=2
    || type.reloadMultiplier!=1 || type.range<block.range) throw new Error("graphite stats changed");
 if(type.pierce || type.splashDamage!=0 || type.homingPower!=0) throw new Error("unexpected graphite effects");
 function hit(unitType,angle,bulletType) {
   var u=unitType.create(Team.crux); u.set(128,128); u.armor=0; u.vel.setZero();
   var b=Bullet.create(); b.type=bulletType; b.damage=bulletType.damage; b.team=Team.sharded;
   /* Put the bullet off-axis: impact must follow flight, not separation vector. */
   b.set(125,124); b.vel.trns(angle,bulletType.speed);
   var before=u.health; bulletType.hitEntity(b,u,before);
   if(Math.abs(before-u.health-bulletType.damage)>0.001) throw new Error("direct damage changed");
   return u;
 }
 var unitTypes=[UnitTypes.dagger,UnitTypes.fortress,UnitTypes.flare];
 var angles=[0,90,180,270];
 for(var i=0;i<unitTypes.length;i++) {
   for(var j=0;j<angles.length;j++) {
     var u=hit(unitTypes[i],angles[j],type);
     var expected=24/u.mass();
     var ex=Angles.trnsx(angles[j],expected), ey=Angles.trnsy(angles[j],expected);
     if(Math.abs(u.vel.x-ex)>0.0001 || Math.abs(u.vel.y-ey)>0.0001)
       throw new Error("wrong impulse: "+unitTypes[i].name+" angle="+angles[j]+" velocity="+u.vel+" expected="+ex+","+ey);
   }
 }
 var light=hit(UnitTypes.dagger,0,type), heavy=hit(UnitTypes.fortress,0,type);
 if(!(heavy.mass()>light.mass() && heavy.vel.len()<light.vel.len())) throw new Error("mass resistance failed");
 var controls=[Items.copper,Items.silicon,Items.pyratite];
 for(var k=0;k<controls.length;k++) {
   var control=hit(UnitTypes.dagger,0,block.ammoTypes.get(controls[k]));
   if(control.vel.len()>0.00001) throw new Error("other ammo gained knockback: "+controls[k].name);
 }
 var build=block.newBuilding().create(block,Team.sharded);
 build.handleStack(Items.graphite,30,null);
 if(build.totalAmmo!=60 || build.acceptItem(null,Items.graphite) || build.useAmmo()!=type || build.totalAmmo!=59)
   throw new Error("graphite ammo economy changed");
 var victim=UnitTypes.dagger.create(Team.crux); victim.set(128,128); victim.armor=0; victim.vel.setZero();
 var actual=type.create(build,Team.sharded,124,128,0); var health=victim.health;
 actual.collision(victim,victim.x,victim.y);
 if(Math.abs(health-victim.health-18)>0.001 || Math.abs(victim.vel.x-24/victim.mass())>0.0001
    || Math.abs(victim.vel.y)>0.0001 || actual.isAdded()) throw new Error("actual projectile collision failed");
 print("MOD_CHECK_PASS: 12 impact directions/masses, actual collision, air/ground, damage, heavy resistance, other-ammo controls and magazine verified; dagger="+light.vel.len()+", fortress="+heavy.vel.len());
} catch(error) { print("MOD_CHECK_FAIL: "+error); }
'''

if __name__ == "__main__":
    raise SystemExit(check_mod.main())
