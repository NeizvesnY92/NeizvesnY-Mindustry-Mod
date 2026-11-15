# NeizvesnY Copper Power Plant — validation

## Intended behavior

- Mindustry v136 block type: `ConsumeGenerator`.
- Footprint: 3x3; sprite: 96x96 pixels (32 pixels per tile).
- Fuel: copper only, 1 item per 120 ticks (2 seconds).
- Output: 4.0 power/tick at 100% efficiency, equivalent to 240 power/second.
- Capacity: 20 copper.
- Research parent: vanilla `combustion-generator`.

The output is four times the vanilla Combustion Generator (1.0 power/tick). It is intentionally a strong mid-game power option, but it does not accept coal, pyratite or other fuels.

## Automated checks

`tools/check_assets.py` validates the 96x96 PNG, its decoded scanlines and both Russian localization bundles.

`tools/check_mod.py` loads the mod in the official Mindustry v136 server and verifies the block exists, is a `ConsumeGenerator`, has the expected research parent, produces 4.0 power/tick and burns each item for 120 ticks.

## Manual iPhone test still required

1. Import the feature branch ZIP or repository into Mindustry v136.
2. Unlock the block and confirm its 3x3 footprint and sprite alignment.
3. Insert copper only; confirm 1 copper is consumed every 2 seconds.
4. Connect it to a power network and confirm output reaches 240 power/second at full efficiency.
5. Disconnect/reconnect power consumers, save, reload and confirm fuel progress and output behave normally.

Automated headless validation cannot confirm visual effects, touch UI, actual network behavior or save/reload behavior on the iPhone.
