#!/usr/bin/env python3
"""Exercise native Bulwark bullet reflection on Mindustry v136."""
import check_mod

check_mod.CHECK = r'''
try {
 var block=Vars.content.block("neizvesny-mindustry-mod-neizvesny-bulwark");
 if(block.chanceDeflect!=10 || block.health!=2100 || block.armor!=9 || !block.insulated || !block.absorbLasers)
   throw new Error("wrong Bulwark configuration");
 var phase=0;
 for(var i=0;i<block.requirements.length;i++) if(block.requirements[i].item==Items.phaseFabric) phase=block.requirements[i].amount;
 if(phase!=8) throw new Error("missing phase fabric cost");
 Vars.world.resize(64,64); Vars.world.tiles.fill();
 Vars.world.tile(16,16).setBlock(block,Team.sharded);
 var build=Vars.world.tile(16,16).build;
 var type=new BasicBulletType(3,5);
 function bullet(damage,speed,reflectable) {
   type.reflectable=reflectable;
   var b=Bullet.create(); b.type=type; b.damage=damage; b.team=Team.crux;
   b.set(build.x-5,build.y); b.vel.set(speed,0); b.time=0;
   return b;
 }
 var b=bullet(5,3,true), before=build.health; b.add();
 if(build.collision(b)!==false || b.team!=Team.sharded || b.owner!=build || b.vel.x>=0 || b.vel.y!=0)
   throw new Error("reflectable light bullet was not returned to enemy");
 if(!(build.health<before)) throw new Error("reflection incorrectly prevented wall damage");
 var enemy=UnitTypes.dagger.create(Team.crux), ally=UnitTypes.dagger.create(Team.sharded);
 enemy.set(build.x-20,build.y); ally.set(build.x-20,build.y); enemy.armor=0;
 if(!b.collides(enemy) || b.collides(ally)) throw new Error("reflected target team filters failed");
 var enemyHealth=enemy.health;
 b.collision(enemy,enemy.x,enemy.y);
 if(Math.abs(enemyHealth-enemy.health-5)>0.001 || b.isAdded()) throw new Error("reflected bullet did not damage enemy and stop");
 var fixed=bullet(5,3,false);
 if(build.collision(fixed)!==true || fixed.team!=Team.crux || fixed.vel.x!=3) throw new Error("unreflectable bullet reflected");
 var slow=bullet(5,0.05,true);
 if(build.collision(slow)!==true || slow.team!=Team.crux) throw new Error("slow bullet reflected");
 var reflected=0, stopped=0;
 Mathf.rand.setSeed(12345);
 for(var n=0;n<100;n++) {
   build.health=block.health;
   var heavy=bullet(100,3,true);
   if(build.collision(heavy)===false) reflected++; else stopped++;
 }
 if(reflected==0 || stopped==0) throw new Error("strong shots must be probabilistic: "+reflected+"/"+stopped);
 var wall=Vars.content.block("neizvesny-mindustry-mod-neizvesny-wall");
 if(wall.chanceDeflect>0 || wall.health!=480 || wall.armor!=5) throw new Error("small wall changed");
 print("MOD_CHECK_PASS: reflection, team, owner, reversed velocity, enemy damage, ally filter, wall damage, excluded bullets, phase cost; heavy reflected="+reflected+", stopped="+stopped);
} catch(error) { print("MOD_CHECK_FAIL: "+error); }
'''

if __name__ == "__main__":
    raise SystemExit(check_mod.main())
