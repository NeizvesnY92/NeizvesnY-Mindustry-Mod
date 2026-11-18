#!/usr/bin/env python3
"""Exercise the copper-only generator fuel contract on Mindustry v136."""
import check_mod

check_mod.CHECK = r'''
try {
  var block = Vars.content.block("neizvesny-mindustry-mod-neizvesny-copper-power-plant");
  if (block == null || !(block instanceof ConsumeGenerator))
    throw new Error("copper power plant did not load as ConsumeGenerator");
  if (block.itemCapacity !== 20)
    throw new Error("wrong item capacity: expected 20 copper, got " + block.itemCapacity);
  if (!block.hasItems || !block.acceptsItems)
    throw new Error("generator does not expose its fuel inventory");

  var itemConsumer = null;
  var itemConsumerCount = 0;
  for (var i = 0; i < block.consumers.length; i++) {
    var consumer = block.consumers[i];
    if (String(consumer.getClass().getSimpleName()) === "ConsumeItems") {
      itemConsumer = consumer;
      itemConsumerCount++;
    }
  }
  if (itemConsumerCount !== 1)
    throw new Error("expected exactly one item-fuel consumer, got " + itemConsumerCount);

  var fuel = itemConsumer.items;
  if (fuel.length !== 1 || fuel[0].item !== Items.copper || fuel[0].amount !== 1)
    throw new Error("generator must consume exactly 1 copper and no other item");

  if (Items.copper.id >= block.itemFilter.length || !block.itemFilter[Items.copper.id])
    throw new Error("copper is missing from the generator input filter");
  for (var itemId = 0; itemId < block.itemFilter.length; itemId++) {
    if (block.itemFilter[itemId] && itemId !== Items.copper.id)
      throw new Error("generator unexpectedly accepts item ID " + itemId);
  }

  var build = block.newBuilding().create(block, Team.sharded);
  if (!build.acceptItem(null, Items.copper))
    throw new Error("generator rejects copper");
  var rejected = [Items.lead, Items.coal, Items.graphite, Items.silicon, Items.pyratite, Items.thorium];
  for (var r = 0; r < rejected.length; r++) {
    if (build.acceptItem(null, rejected[r]))
      throw new Error("generator unexpectedly accepts " + rejected[r].name);
  }
  if (itemConsumer.efficiency(build) !== 0)
    throw new Error("empty generator reports valid fuel");

  build.handleItem(null, Items.copper);
  build.handleItem(null, Items.copper);
  if (build.items.get(Items.copper) !== 2)
    throw new Error("failed to insert two copper items");

  var previousDelta = Time.delta;
  var previousEffectChance = block.effectChance;
  Time.delta = 1;
  block.effectChance = 0;

  function tick() {
    build.efficiency = itemConsumer.efficiency(build);
    build.potentialEfficiency = build.efficiency;
    build.updateTile();
  }

  tick();
  if (build.items.get(Items.copper) !== 1)
    throw new Error("first active tick did not consume exactly one copper");
  if (Math.abs(build.generateTime - (1 - 1 / 120)) > 0.0001)
    throw new Error("fuel cycle did not start at 120 ticks: " + build.generateTime);
  if (Math.abs(build.getPowerProduction() - 4.0) > 0.001)
    throw new Error("full-efficiency output is not 4 power/tick");

  for (var t = 0; t < 119; t++) tick();
  if (build.items.get(Items.copper) !== 1)
    throw new Error("generator consumed fuel before the 120-tick cycle ended");
  if (Math.abs(build.generateTime) > 0.001)
    throw new Error("first fuel cycle did not finish after 120 ticks: " + build.generateTime);

  tick();
  if (build.items.get(Items.copper) !== 0)
    throw new Error("second fuel item was not consumed at the next cycle");
  if (Math.abs(build.generateTime - (1 - 1 / 120)) > 0.0001)
    throw new Error("second fuel cycle did not restart correctly");

  for (var idle = 0; idle < 120; idle++) tick();
  if (itemConsumer.efficiency(build) !== 0 || build.getPowerProduction() !== 0)
    throw new Error("generator continues producing after its last fuel expires");
  if (build.items.get(Items.copper) !== 0)
    throw new Error("generator created or retained unexpected fuel");

  Time.delta = previousDelta;
  block.effectChance = previousEffectChance;
  print("MOD_CHECK_PASS: copper-only filter, 20-item capacity, exact 1-copper consumer, 120-tick burn, 4 power/tick, depletion and rejected fuels verified");
} catch (error) {
  print("MOD_CHECK_FAIL: " + error);
}
'''

if __name__ == "__main__":
    raise SystemExit(check_mod.main())
