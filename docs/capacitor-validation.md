# NeizvesnY Capacitor — validation

## Intended behavior

- Mindustry v136 native block type: `Battery`.
- Footprint: 2x2; main sprite and `-top` overlay: 64x64 pixels each.
- Buffered power capacity: 12,000 power units.
- Uses the native `powerBuffered` consumer; it stores surplus power in the connected graph and discharges when the graph needs power.
- It does not generate power and does not consume items.
- Build cost: 90 copper, 70 lead, 35 graphite and 20 silicon.
- Research parent: NeizvesnY Copper Power Plant.

The 12,000-unit capacity is three times the vanilla small Battery (4,000) and below the vanilla large Battery (50,000). Its 2x2 footprint and mid-tier material cost place it between the two vanilla sizes.

## Automated checks

`tools/check_mod.py` loads the mod in the official Mindustry v136 server and verifies the native Battery type, buffered power consumer, exact capacity, power input/output flags and research parent.

`tools/check_assets.py` validates both 64x64 sprite layers, PNG decoding and both Russian localization bundles. The asset checker now requires a `-top.png` layer for every block whose type is `Battery`.

## Manual iPhone test still required

1. Import the branch ZIP or repository into Mindustry v136.
2. Unlock the Capacitor after the NeizvesnY Copper Power Plant and confirm its 2x2 footprint and top overlay.
3. Connect it to the copper generator and a power consumer; confirm surplus energy charges the battery.
4. Reduce generation or increase demand; confirm stored power discharges into the same graph.
5. Disconnect and reconnect power nodes; confirm the battery joins the intended network without bridging separate teams.
6. Save and reload while partially charged; confirm the stored charge persists and the sprite's native charge indicator matches it.

Headless v136 checks validate loaded block properties, not the rendered indicator, live power-graph behavior or a full iPhone save/reload.
