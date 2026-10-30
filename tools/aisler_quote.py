#!/usr/bin/env python3
"""Aisler-style PCB price estimate for this board.

Aisler publishes its pricing as a formula rather than a REST API:
    PCB price = job fee + area x area-usage fee x quantity
(2-layer, 1.6 mm, HASL "Budget": €12.00 job fee, €0.067/cm², minimum 3 pcs).

Programmatic *live* quotes need an Aisler access key (granted case by case via
their support form) and their MCP server at https://aisler.net/mcp — set
AISLER_MCP_URL/AISLER_TOKEN to enable that path; until then this script uses the
published formula so numbers are reproducible offline.

Usage
-----
    python3 tools/aisler_quote.py --width 46 --height 89 --qty 5
    python3 tools/aisler_quote.py --pcb hardware/esp32-c3-sensor-board-rev2.kicad_pcb --qty 5
    python3 tools/aisler_quote.py --pcb ... --qty 5 --json

Exit code 0 on success, 2 on bad input. No third-party dependencies.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass, asdict

# Published Aisler "Budget" tier, 2 layers, 1.6 mm, HASL, green.
JOB_FEE_EUR = 12.00
AREA_FEE_EUR_PER_CM2 = 0.067
MIN_QTY = 3
SHIPPING_EUR = 4.90          # EU flat, estimate only

# Optional extras (estimates; confirm in the Aisler UI before ordering)
THICKNESS_UPLIFT = {1.6: 0.0}
FINISH_UPLIFT = {"HASL": 0.0, "ENIG": 0.15}   # fraction of board price


@dataclass
class Quote:
    width_mm: float
    height_mm: float
    area_cm2: float
    qty: int
    finish: str
    board_total_eur: float
    board_each_eur: float
    shipping_eur: float
    delivered_total_eur: float
    delivered_each_eur: float

    def as_row(self) -> str:
        return (f"{self.qty:>3} pcs  {self.width_mm:.1f}x{self.height_mm:.1f} mm  "
                f"{self.area_cm2:6.2f} cm²  {self.finish:<4}  "
                f"board €{self.board_total_eur:6.2f} (€{self.board_each_eur:5.2f}/pc)  "
                f"delivered €{self.delivered_total_eur:6.2f} (€{self.delivered_each_eur:5.2f}/pc)")


def board_size_from_pcb(path: str) -> tuple[float, float]:
    """Read the Edge.Cuts extents from a .kicad_pcb without needing pcbnew."""
    text = open(path, encoding="utf-8", errors="ignore").read()
    xs: list[float] = []
    ys: list[float] = []
    for m in re.finditer(r"\(gr_(?:line|arc|rect)\b", text):
        i = m.start()
        depth = 0
        j = i
        while j < len(text):
            if text[j] == "(":
                depth += 1
            elif text[j] == ")":
                depth -= 1
                if depth == 0:
                    j += 1
                    break
            j += 1
        block = text[i:j]
        if '"Edge.Cuts"' not in block:
            continue
        for sm in re.finditer(r"\(start\s+([-\d.]+)\s+([-\d.]+)\)", block):
            xs.append(float(sm.group(1)))
            ys.append(float(sm.group(2)))
        for em in re.finditer(r"\(end\s+([-\d.]+)\s+([-\d.]+)\)", block):
            xs.append(float(em.group(1)))
            ys.append(float(em.group(2)))
    if not xs:
        raise ValueError("no Edge.Cuts geometry found")
    return max(xs) - min(xs), max(ys) - min(ys)


def quote(width: float, height: float, qty: int, finish: str) -> Quote:
    area = (width / 10.0) * (height / 10.0)
    qty = max(qty, MIN_QTY)
    board = JOB_FEE_EUR + area * AREA_FEE_EUR_PER_CM2 * qty
    board *= 1.0 + FINISH_UPLIFT.get(finish.upper(), 0.0)
    return Quote(width, height, area, qty, finish.upper(),
                 round(board, 2), round(board / qty, 2),
                 SHIPPING_EUR, round(board + SHIPPING_EUR, 2),
                 round((board + SHIPPING_EUR) / qty, 2))


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Estimate Aisler PCB price for this board")
    ap.add_argument("--pcb", help="KiCad board file; board size is read from Edge.Cuts")
    ap.add_argument("--width", type=float, help="board width in mm")
    ap.add_argument("--height", type=float, help="board height in mm")
    ap.add_argument("--qty", type=int, default=5)
    ap.add_argument("--finish", default="HASL", choices=["HASL", "ENIG"])
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    args = ap.parse_args(argv)

    if args.pcb:
        width, height = board_size_from_pcb(args.pcb)
    elif args.width and args.height:
        width, height = args.width, args.height
    else:
        ap.error("give --pcb or --width/--height")

    q = quote(width, height, args.qty, args.finish)
    if args.json:
        print(json.dumps(asdict(q), indent=2))
    else:
        print("Aisler estimate (published Budget formula, no live API)")
        print(q.as_row())
        print(f"       job fee €{JOB_FEE_EUR:.2f} + {AREA_FEE_EUR_PER_CM2} €/cm² x qty"
              f" (min {MIN_QTY} pcs), shipping assumed €{SHIPPING_EUR:.2f}")
        if os.environ.get("AISLER_TOKEN"):
            print("note: AISLER_TOKEN is set — live quoting needs the Aisler MCP "
                  "server (https://aisler.net/mcp); this script does not call it yet.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        raise SystemExit(2)
