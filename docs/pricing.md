# Cost estimate — bare PCB vs fully populated

Numbers are **estimates** unless marked *live*. Aisler numbers come from the
live project (`BEAGDVXB`) via the Aisler MCP; JLCPCB and PCBWay numbers are
calculated from their published PCB pricing and the LCSC price breaks, because
neither exposes a public quote API. Re-check at order time.

Aisler's bare-PCB price is a formula:

```
PCB price = job fee + area × area-usage fee × quantity
2 layers, 1.6 mm, HASL "Budget": €12.00 job fee + €0.067/cm², minimum 3 pcs
```

## Board

| | |
|---|---|
| Size | 46 × 89 mm = **40.94 cm²** |
| Layers / material | 2, FR4 1.6 mm, 1 oz |
| Finish | HASL or ENIG |
| Assembly | THT sockets/headers/terminal; J3 hand-soldered; 3 shunts hand-fitted |

## Bare PCB (5 pieces)

| Source | Board total | Unit price | Notes |
|---|---|---|---|
| Aisler, HASL | **€25.71** | **€5.14** | formula; +€4.90 shipping → €6.12/pc delivered |
| Aisler, ENIG | €29.57 | €5.91 | +15 % finish uplift (estimate) |
| JLCPCB (typical) | $9–15 | $1.8–3.0 | 2-layer, HASL; shipping and VAT dominate |
| PCBWay (typical) | $25–35 | $5–7 | 2-layer, HASL; includes their larger-board pricing |

## Assembly BOM (5 boards)

The 10 assembled lines are the sockets, headers and screw terminal. J3 is
excluded from every provider assembly BOM/CPL (hand-soldered); the three
2.54 mm shunts are hand-fitted and have no CAD footprint.

### Aisler — live BOM from the MCP

| Designator | Part | MPN | LCSC | Qty/board |
|---|---|---|---|---|
| U1A, U1B | 1×8 female socket | BOOMELE 2.54-1*8P | C27438 | 2 |
| U2, J2 | 1×5 female socket | BOOMELE 2.54-1*5P | C50950 | 2 |
| J1 | 1×6 female socket | BOOMELE 2.54-1*6P | C40877 | 1 |
| J4 | 2P 5.0 mm screw terminal | MAX MX126-5.0-02P-GN01-Cu-S-A | C5188434 | 1 |
| J5 | 1×14 female socket | Samtec SSW-114-01-T-S | C41417326* | 1 |
| JP1, JP2 | 1×3 pin header | Samtec TSW-103-07-G-S | C49257 | 2 |
| JP3 | 1×2 pin header | hanxia HX PZ2.54-1x2P ZZ | C32713268 | 1 |
| J3 | 1×3 right-angle socket | **excluded — hand-solder** | C54876732 | 1 |
| SHUNT | 2.54 mm jumper shunt | **not in CAD BOM — hand-fit** | C5305 | 3 |

\* Aisler's catalogue does not carry LCSC C41417326; it quotes the Samtec
SSW-114-01-T-S instead. The other lines use the LCSC part that Aisler's
catalogue maps to the same MPN.

Aisler live BOM, **one board, minimum order quantities** (MCP
`update_bill_of_material_status`):

| MPN | Extended price | Procurement qty |
|---|---|---|
| MX126-5.0-02P-GN01-Cu-S-A | €0.56 | 10 |
| 2.54-1*8P | €0.53 | 5 |
| 2.54-1*5P | €0.77 | 10 |
| 2.54-1*6P | €0.40 | 5 |
| SSW-114-01-T-S | €3.02 | 3 |
| TSW-103-07-G-S | €1.93 | 10 |
| HX PZ2.54-1x2P ZZ | €0.07 | 5 |
| **Parts total (MOQ)** | **€7.28** | |

That €7.28 is dominated by MOQ and Samtec cut-tape pricing. At **5 boards** the
same BOM needs about €10–11 of parts (roughly €2.1/board), plus J3 and shunts.

### JLCPCB / PCBWay — LCSC BOM (5 boards)

| Designator | LCSC | Qty (5 boards) | LCSC unit | Extended |
|---|---|---|---|---|
| U1A, U1B | C27438 | 10 | $0.1005 | $1.01 |
| U2, J2 | C50950 | 10 | $0.0856 | $0.86 |
| J1 | C40877 | 5 | $0.0892 | $0.45 |
| J4 | C5188434 | 5 | $0.0631 | $0.32 |
| J5 | C41417326 | 5 | ~$0.30 (est.) | ~$1.50 |
| JP1, JP2 | C49257 | 10 | $0.0292 | $0.29 |
| JP3 | C32713268 | 5 | ~$0.014 (est.) | ~$0.07 |
| J3 (hand-solder) | C54876732 | 5 | ~$0.15 (est.) | ~$0.75 |
| SHUNT (hand-fit) | C5305 | 15 | $0.0099 | $0.15 |
| **Parts total** | | | | **~$5.40** |

The same LCSC cart serves JLCPCB and PCBWay. JLCPCB's assembly adds an
extended-part fee (about $3 per non-basic part) and a setup fee; PCBWay quotes
THT assembly per job. At 5 boards those fees dominate the parts cost.

## Three-vendor comparison (5 boards, THT assembly)

| Vendor | Bare PCB | Parts | Board + parts | Notes |
|---|---|---|---|---|
| **Aisler** | €25.71 | ~€10–11 | **~€36–37** (€7.20–7.40/board) | Live BOM assigned; assembly quote in project `BEAGDVXB` |
| **JLCPCB** | ~$15 | ~$5.40 | **~$20.40** (~€18.80; €3.80/board) | Extended-part + setup fees are extra; THT assembly limited |
| **PCBWay** | ~$35 | ~$5.40 | **~$40.40** (~€37.20; €7.40/board) | THT assembly quoted per job; shipping higher |

Board + parts only — no assembly labour. At five units the assembly setup
fees (roughly €20–60 depending on vendor and part count) are larger than the
parts themselves, so the hand-built route below remains the cheapest.

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

## Caveats

- Only the Aisler BOM is a live quote. JLCPCB and PCBWay figures are built from
  their published PCB pricing and LCSC price breaks; confirm in their
  calculators before ordering.
- Part prices are indicative; shipping and VAT are excluded from the parts
  lines. Aisler shows USD price breaks from LCSC/Farnell/Mouser/Digi-Key and
  converts them.
- J3 is deliberately excluded from provider assembly: it must be raised to
  meet the KY-019 relay header. See
  [`fabrication/assembly/hand-solder-j3.md`](../fabrication/assembly/hand-solder-j3.md).
- The three jumper shunts are hand-fitted; they have no CAD footprint and
  therefore no provider placement line.
- The five plug-in modules are not part of any assembly BOM.
