#!/usr/bin/env python3
"""KiCad API plugin: build a PCB quote report for the open board.

KiCad launches this entrypoint with KICAD_API_SOCKET / KICAD_API_TOKEN set.
It connects with kipy, reads the open board's file path, builds an HTML report
containing an offline Aisler estimate and links to the quote/upload pages of
Aisler, JLCPCB, PCBWay, Eurocircuits and OSHPark, then opens it in the default
browser.

No GUI toolkit is used: the report is a self-contained HTML file, so it works
from the isolated Python environment that KiCad creates for API plugins
(requirements.txt pulls in kicad-python / kipy).
"""

from __future__ import annotations

import datetime
import html
import json
import os
import re
import subprocess
import sys
import tempfile
import webbrowser
from pathlib import Path

PROVIDERS = [
    ("Aisler", "https://aisler.net/", "Offline estimate below"),
    ("JLCPCB", "https://cart.jlcpcb.com/quote", "Upload gerber zip"),
    ("PCBWay", "https://www.pcbway.com/orderonline.aspx", "Upload gerber zip"),
    ("Eurocircuits", "https://www.eurocircuits.com/", "Upload gerber zip"),
    ("OSHPark", "https://oshpark.com/", "Upload gerber zip"),
]

CSS = """
:root { color-scheme: light dark; }
body { font: 15px/1.55 -apple-system, BlinkMacSystemFont, "Segoe UI", system-ui, sans-serif;
       max-width: 880px; margin: 36px auto; padding: 0 20px; }
h1 { font-size: 26px; margin: 0 0 4px; }
h2 { font-size: 16px; margin: 0 0 10px; }
.sub { opacity: .65; margin: 0 0 22px; }
.card { border: 1px solid rgba(128,128,128,.35); border-radius: 12px;
        padding: 16px 20px; margin: 14px 0; }
.grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
        gap: 10px; }
a.btn { display: block; padding: 11px 14px; border-radius: 9px; background: #2b6cb0;
        color: #fff; text-align: center; text-decoration: none; font-weight: 600; }
a.btn small { display: block; font-weight: 400; opacity: .8; font-size: 11px; }
a { color: #2b6cb0; }
table { border-collapse: collapse; width: 100%; }
th, td { text-align: left; padding: 6px 8px; border-bottom: 1px solid rgba(128,128,128,.25); }
pre { background: rgba(128,128,128,.12); padding: 12px; border-radius: 8px;
      overflow-x: auto; font-size: 13px; }
"""


def find_repo_root(board_path: str) -> Path:
    p = Path(board_path).resolve().parent
    for _ in range(6):
        if (p / "tools" / "aisler_quote.py").exists():
            return p
        if p.parent == p:
            break
        p = p.parent
    return Path(board_path).resolve().parent.parent


def board_size_mm(board_path: str):
    """Read the Edge.Cuts extents without needing pcbnew."""
    text = open(board_path, encoding="utf-8", errors="ignore").read()
    xs, ys = [], []
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
        return None
    return max(xs) - min(xs), max(ys) - min(ys)


def aisler_estimates(board_path: str, repo_root: Path):
    script = repo_root / "tools" / "aisler_quote.py"
    if not script.exists():
        return {}
    out = {}
    for finish in ("HASL", "ENIG"):
        try:
            proc = subprocess.run(
                [sys.executable, str(script), "--pcb", board_path, "--qty", "5",
                 "--finish", finish, "--json"],
                capture_output=True, text=True, timeout=30,
            )
            if proc.returncode == 0:
                out[finish] = json.loads(proc.stdout)
        except Exception:
            pass
    return out


def render_html(board_path: str, estimate: dict, repo_root: Path) -> str:
    name = html.escape(os.path.basename(board_path))
    size = board_size_mm(board_path)
    if size:
        width, height = size
        area = width * height / 100.0
        size_row = f"{width:.1f} &times; {height:.1f} mm &nbsp;·&nbsp; {area:.2f} cm²"
    else:
        width = height = area = None
        size_row = "size unavailable"

    rows = []
    for finish in ("HASL", "ENIG"):
        e = estimate.get(finish)
        if e:
            rows.append(
                f"<tr><td>{finish}</td><td>€{e['board_total_eur']:.2f}</td>"
                f"<td>€{e['delivered_total_eur']:.2f}</td>"
                f"<td>€{e['delivered_each_eur']:.2f}</td></tr>"
            )
    if not rows:
        rows.append('<tr><td colspan="4">Aisler estimate unavailable '
                    '(tools/aisler_quote.py not found next to the board).</td></tr>')

    provider_cards = "\n".join(
        f'<a class="btn" href="{html.escape(url)}" target="_blank" rel="noopener">'
        f'{html.escape(label)}<small>{html.escape(note)}</small></a>'
        for label, url, note in PROVIDERS
    )

    fab_dir = repo_root / "fabrication"
    zip_path = next(iter(sorted(fab_dir.glob("*gerbers.zip"))), None) if fab_dir.is_dir() else None
    fab_links = []
    if fab_dir.is_dir():
        fab_links.append(f'<a href="{fab_dir.as_uri()}">fabrication folder</a>')
    if zip_path:
        fab_links.append(f'<a href="{zip_path.as_uri()}">{html.escape(zip_path.name)}</a>')
    fab_links_html = " · ".join(fab_links) or "fabrication folder not found"

    summary_lines = [os.path.basename(board_path)]
    if width is not None:
        summary_lines.append(f"Size: {width:.1f} x {height:.1f} mm ({area:.2f} cm2)")
    summary_lines += [
        "Layers: 2",
        "Material / thickness: FR4, 1.6 mm",
        "Copper weight: 1 oz",
        "Min trace / clearance: 0.15 mm / 0.2 mm",
        "Min drill: 0.3 mm (vias 0.7/0.3)",
        "Surface finish: ENIG preferred (HASL lead-free acceptable)",
        "Solder mask: green, both sides",
        "Silkscreen: white, both sides",
        "Impedance control: not required",
    ]
    summary = html.escape("\n".join(summary_lines))
    generated = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>PCB quote — {name}</title>
<style>{CSS}</style></head><body>
<h1>PCB quote</h1>
<p class="sub">{name} &nbsp;·&nbsp; {size_row} &nbsp;·&nbsp; generated {generated}</p>

<div class="card">
  <h2>Aisler estimate (5 pcs)</h2>
  <table>
    <tr><th>Finish</th><th>Board</th><th>Delivered</th><th>Per piece</th></tr>
    {''.join(rows)}
  </table>
  <p class="sub">Published Budget formula, offline estimate; shipping assumed €4.90.
  Confirm in the vendor's calculator before ordering.</p>
</div>

<div class="card">
  <h2>Request a quote</h2>
  <div class="grid">{provider_cards}</div>
  <p class="sub" style="margin-top:12px">Gerber package: {fab_links_html}</p>
</div>

<div class="card">
  <h2>Board summary for vendor forms</h2>
  <pre>{summary}</pre>
</div>
</body></html>
"""


def main() -> int:
    try:
        from kipy import KiCad
    except Exception as exc:  # pragma: no cover - environment problem
        print(f"PCB Quote: kipy is not available: {exc}", file=sys.stderr)
        return 1

    try:
        kicad = KiCad()
        board = kicad.get_board()
    except Exception as exc:
        print(f"PCB Quote: could not reach the open board: {exc}", file=sys.stderr)
        return 1

    board_path = os.path.expanduser(board.name or "")
    if not board_path or not os.path.exists(board_path):
        print("PCB Quote: the board has not been saved to disk yet", file=sys.stderr)
        return 1

    repo_root = find_repo_root(board_path)
    report = render_html(board_path, aisler_estimates(board_path, repo_root), repo_root)
    out = Path(tempfile.gettempdir()) / "kicad-pcb-quote.html"
    out.write_text(report, encoding="utf-8")
    webbrowser.open(out.as_uri())

    size = board_size_mm(board_path)
    if size:
        print(f"PCB Quote: {os.path.basename(board_path)} "
              f"{size[0]:.1f} x {size[1]:.1f} mm — report: {out}")
    else:
        print(f"PCB Quote: report: {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
