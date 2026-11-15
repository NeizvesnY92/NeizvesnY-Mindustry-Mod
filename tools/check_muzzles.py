#!/usr/bin/env python3
"""Check Bastion's actual shot origins against its unchanged 96px sprite."""
import check_mod

check_mod.CHECK = r'''
try {
 var block=Vars.content.block("neizvesny-mindustry-mod-neizvesny-bastion");
 /* Sprite pixel boundaries: barrels x=[27,43), [57,74), top y=6. */
 /* 4 pixels/world unit; texture origin (48,48). Centers: 35,65.5. */
 var muzzleX=[-3.25,4.375], muzzleY=10.5;
 var items=[Items.copper,Items.graphite,Items.silicon,Items.blastCompound,Items.thorium];
 var rotations=[0,45,90,180,225,270];
 Time.delta=1;
 for(var a=0;a<items.length;a++) {
   for(var r=0;r<rotations.length;r++) {
     var build=block.newBuilding().create(block,Team.sharded);
     build.set(256,256); build.rotation=rotations[r];
     build.targetPos.set(256+Angles.trnsx(build.rotation,200),256+Angles.trnsy(build.rotation,200));
     build.logicControlTime=120; build.logicShooting=true;
     build.efficiency=1; build.potentialEfficiency=1;
     build.handleStack(items[a],5,null);
     var initialAmmo=build.totalAmmo;
     for(var shot=0;shot<2;shot++) {
       Groups.bullet.clear();
       build.reloadCounter=block.reload;
       build.updateTile();
       if(Groups.bullet.size()!=1 || build.totalShots!=shot+1)
         throw new Error("expected one bullet per alternating shot");
       var bullet=Groups.bullet.index(0);
       if(bullet.type!=block.ammoTypes.get(items[a])) throw new Error("wrong ammo type");
       /* Native BulletType.create backdates the bullet by one velocity*delta. */
       var originX=bullet.x+bullet.vel.x*Time.delta;
       var originY=bullet.y+bullet.vel.y*Time.delta;
       var expectedX=build.x+Angles.trnsx(build.rotation-90,muzzleX[shot],muzzleY);
       var expectedY=build.y+Angles.trnsy(build.rotation-90,muzzleX[shot],muzzleY);
       if(Math.abs(originX-expectedX)>0.001 || Math.abs(originY-expectedY)>0.001)
         throw new Error("muzzle mismatch: "+items[a].name+" rotation="+build.rotation+" barrel="+shot
                         +" expected="+expectedX+","+expectedY+" actual="+originX+","+originY);
       if(build.totalAmmo!=initialAmmo-shot-1) throw new Error("wrong ammo consumption");
     }
   }
 }
 Groups.bullet.clear();
 print("MOD_CHECK_PASS: 60 actual Bastion shots, both sprite muzzles, six rotations, five ammo types and consumption verified");
} catch(error) { print("MOD_CHECK_FAIL: "+error); }
'''

if __name__ == "__main__":
    raise SystemExit(check_mod.main())
