#!/usr/bin/env python3
"""Exercise optional Sentinel cooling on the loaded Mindustry engine."""
import check_mod

check_mod.CHECK = r'''
try {
 var block=Vars.content.block("neizvesny-mindustry-mod-neizvesny-sentinel");
 if(block.coolant == null || !block.coolant.optional || !block.coolant.booster) throw new Error("coolant is not optional booster");
 if(!block.hasLiquids || block.liquidCapacity != 20 || Math.abs(block.coolant.amount-0.1)>0.00001) throw new Error("wrong liquid configuration");
 var build=block.newBuilding().create(block,Team.sharded);
 build.handleStack(Items.copper,5,null);
 build.efficiency=1; build.potentialEfficiency=1;
 Time.delta=1;
 if(!build.acceptLiquid(null,Liquids.water) || !build.acceptLiquid(null,Liquids.cryofluid)) throw new Error("coolant rejected");
 if(build.acceptLiquid(null,Liquids.slag) || build.acceptLiquid(null,Liquids.oil)) throw new Error("unsafe liquid accepted");
 function step(liquid){
   build.liquids.clear();
   if(liquid != null) build.liquids.add(liquid,10);
   build.reloadCounter=0;
   build.updateTile();
   return build.reloadCounter;
 }
 var dry=step(null), water=step(Liquids.water), cryo=step(Liquids.cryofluid);
 if(Math.abs(dry-1)>0.00001) throw new Error("dry reload changed: "+dry);
 if(Math.abs(water-1.2)>0.0001 || Math.abs(cryo-1.45)>0.0001) throw new Error("wrong reload increments: "+water+", "+cryo);
 if(Math.abs(build.liquids.get(Liquids.cryofluid)-9.9)>0.0001) throw new Error("wrong coolant usage");
 build.reloadCounter=block.reload;
 build.updateTile();
 if(Math.abs(build.liquids.get(Liquids.cryofluid)-9.9)>0.0001) throw new Error("coolant wasted when fully loaded");
 build.liquids.clear(); build.liquids.add(Liquids.water,0.1); build.reloadCounter=0;
 build.updateTile(); var before=build.reloadCounter;
 build.updateTile();
 if(Math.abs(build.reloadCounter-before-dry)>0.0001) throw new Error("dry fallback after depletion failed");
 if(build.totalAmmo != 10 || block.reload != 9 || block.maxAmmo != 60) throw new Error("ammo or base reload changed");
 print("MOD_CHECK_PASS: dry=1 water=1.2 cryofluid=1.45, liquid filtering, usage, idle and depletion verified");
} catch(error){ print("MOD_CHECK_FAIL: "+error); }
'''

if __name__ == "__main__":
    raise SystemExit(check_mod.main())
