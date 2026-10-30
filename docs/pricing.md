# Cost estimate — bare PCB vs fully populated

Numbers are **estimates**, generated with [`tools/aisler_quote.py`](../tools/aisler_quote.py)
and hand-entered part prices. Re-run the script after any board change.

Aisler does not publish a REST pricing endpoint; their pricing is a formula:

```
PCB price = job fee + area × area-usage fee × quantity
2 layers, 1.6 mm, HASL "Budget": €12.00 job fee + €0.067/cm², minimum 3 pcs
```

Live quotes require an Aisler access key (granted case by case) and their MCP
server at `https://aisler.net/mcp`; the script uses the formula so results are
reproducible offline.

## Board

| | |
|---|---|
| Size | 46 × 89 mm = **40.94 cm²** |
| Layers / material | 2, FR4 1.6 mm, 1 oz |
| Finish | HASL or ENIG |

## Bare PCB (5 pieces)

| Source | Unit price | Total (5 pcs) | Notes |
|---|---|---|---|
| Aisler, HASL | **€5.14** | €25.71 | formula + 4.90 shipping = €6.12/pc delivered |
| Aisler, ENIG | €5.91 | €29.57 | +15 % finish uplift (estimate) |
| JLCPCB (typical) | €2–3.5 | €10–18 | board ~$2, shipping and VAT dominate |

The script output:

```
5 pcs  46.0x89.0 mm  40.94 cm²  HASL  board €25.71 (€5.14/pc)  delivered €30.61 (€6.12/pc)
5 pcs  46.0x89.0 mm  40.94 cm²  ENIG  board €29.57 (€5.91/pc)  delivered €34.47 (€6.89/pc)
```

## Fully populated (5 pieces, hand assembly)

| Line | Unit | Qty | Ext. |
|---|---|---|---|
| ESP32-C3 Super Mini | €3.00 | 1 | €3.00 |
| HLK-LD2410C | €3.50 | 1 | €3.50 |
| BME280 module | €2.50 | 1 | €2.50 |
| BH1750 GY-302 | €1.50 | 1 | €1.50 |
| KY-019 relay module | €1.00 | 1 | €1.00 |
| Sockets, headers, shunts, terminal | €2.50 | 1 set | €2.50 |
| **Parts subtotal** | | | **€14.00** |
| Bare PCB (Aisler HASL) | €5.14 | 1 | €5.14 |
| **Per unit, hand-built** | | | **≈ €19.10** |
| 5 units, hand-built | | | ≈ €95.50 |

Variants: **BME680** +€5.50/unit (≈ €24.60); **compact / no relay** −€1.00 module and
−1.02 cm² area (≈ €0.07 cheaper board) → ≈ €18.10.

## Assembly by a fabricator

Not quoted: Aisler assembly is priced as setup + per-panel + per-component tasks
and needs an access key; JLCPCB assembly cannot place the modules (not in their
library) and only partially handles the through-hole sockets. At 5 units, hand
assembly is the realistic path.

## Caveats

- Part prices are indicative EU retail; shipping and VAT are excluded from the parts lines.
- The ENIG uplift is an estimate — confirm in the Aisler calculator before ordering.
- The Aisler formula has no shipping/VAT; €4.90 is a placeholder for EU delivery.
