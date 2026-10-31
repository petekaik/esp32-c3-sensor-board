"""KiCad action plugin: PCB quote for the open board.

Shows the board size, an offline Aisler estimate (from tools/aisler_quote.py in
the same repository as the open board), and one-click links to the quote/upload
pages of Aisler, JLCPCB, PCBWay, Eurocircuits and OSHPark.

Install with tools/kicad-plugin/install.py, restart KiCad, then use
Tools -> External Plugins -> PCB Quote (or the toolbar button).
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import webbrowser

import pcbnew  # provided by KiCad

# Vendor quote / upload pages. Only Aisler has an offline estimate here; the
# rest open the vendor's own quote page so you can upload the gerber zip.
PROVIDERS = [
    ("Aisler", "https://aisler.net/"),
    ("JLCPCB", "https://cart.jlcpcb.com/quote"),
    ("PCBWay", "https://www.pcbway.com/orderonline.aspx"),
    ("Eurocircuits", "https://www.eurocircuits.com/"),
    ("OSHPark", "https://oshpark.com/"),
]


def _repo_root_for_board(board_path: str) -> str:
    """The carrier board lives in <repo>/hardware/, so the repo is one level up."""
    return os.path.abspath(os.path.join(os.path.dirname(board_path), os.pardir))


def _board_size_mm(board) -> tuple[float, float]:
    box = board.GetBoardEdgesBoundingBox()
    return pcbnew.ToMM(box.GetWidth()), pcbnew.ToMM(box.GetHeight())


def _aisler_estimate(board_path: str):
    """Run the repo's quote tool and return (dict, None) or (None, error)."""
    script = os.path.join(_repo_root_for_board(board_path), "tools", "aisler_quote.py")
    if not os.path.exists(script):
        return None, f"tools/aisler_quote.py not found at {script}"
    try:
        out = subprocess.run(
            [sys.executable, script, "--pcb", board_path, "--qty", "5", "--json"],
            capture_output=True, text=True, timeout=30,
        )
        if out.returncode != 0:
            return None, (out.stderr or out.stdout).strip()
        return json.loads(out.stdout), None
    except Exception as exc:  # GUI path: report, never crash KiCad
        return None, str(exc)


def _open_path(path: str) -> None:
    if sys.platform == "darwin":
        subprocess.Popen(["open", path])
    elif os.name == "nt":
        os.startfile(path)  # type: ignore[attr-defined]
    else:
        subprocess.Popen(["xdg-open", path])


class QuoteDialog:
    def __init__(self, parent, board_path: str, width: float, height: float,
                 estimate, error):
        import wx

        self.dlg = wx.Dialog(parent, title="PCB quote", size=(600, 470))
        sizer = wx.BoxSizer(wx.VERTICAL)

        title = wx.StaticText(self.dlg, label=os.path.basename(board_path))
        font = title.GetFont()
        font.SetPointSize(font.GetPointSize() + 2)
        font.SetWeight(wx.FONTWEIGHT_BOLD)
        title.SetFont(font)
        sizer.Add(title, 0, wx.ALL, 12)

        sizer.Add(
            wx.StaticText(self.dlg,
                          label=f"Board: {width:.1f} x {height:.1f} mm  |  2 layers  |  "
                                f"FR4 1.6 mm"),
            0, wx.LEFT | wx.RIGHT, 12,
        )

        if estimate:
            txt = (
                "Aisler estimate (published Budget formula, 5 pcs HASL):\n"
                f"board €{estimate['board_total_eur']:.2f}  ·  "
                f"delivered €{estimate['delivered_total_eur']:.2f}  "
                f"(€{estimate['delivered_each_eur']:.2f}/pc)"
            )
        else:
            txt = f"Aisler estimate unavailable: {error}"
        sizer.Add(wx.StaticText(self.dlg, label=txt), 0, wx.ALL, 12)

        box = wx.StaticBoxSizer(wx.VERTICAL, self.dlg, "Open a vendor quote / upload page")
        grid = wx.GridSizer(0, 3, 6, 6)
        for name, url in PROVIDERS:
            btn = wx.Button(box.GetStaticBox(), label=name)
            btn.Bind(wx.EVT_BUTTON, lambda evt, u=url: webbrowser.open(u))
            grid.Add(btn, 0, wx.EXPAND)
        box.Add(grid, 0, wx.EXPAND | wx.ALL, 6)
        sizer.Add(box, 0, wx.EXPAND | wx.ALL, 12)

        sizer.Add(
            wx.StaticText(
                self.dlg,
                label="Aisler is an offline estimate. The other buttons open the vendor's\n"
                      "upload page — upload the gerber zip from the fabrication folder.",
            ),
            0, wx.LEFT | wx.RIGHT, 12,
        )

        row = wx.BoxSizer(wx.HORIZONTAL)
        fab_btn = wx.Button(self.dlg, label="Open fabrication folder")
        fab_btn.Bind(
            wx.EVT_BUTTON,
            lambda evt: _open_path(os.path.join(_repo_root_for_board(board_path),
                                                 "fabrication")),
        )
        close_btn = wx.Button(self.dlg, wx.ID_CLOSE, "Close")
        close_btn.Bind(wx.EVT_BUTTON, lambda evt: self.dlg.EndModal(wx.ID_CLOSE))
        row.Add(fab_btn, 0, wx.RIGHT, 6)
        row.AddStretchSpacer()
        row.Add(close_btn, 0)
        sizer.Add(row, 0, wx.EXPAND | wx.ALL, 12)

        self.dlg.SetSizer(sizer)
        self.dlg.CentreOnParent()

    def show(self) -> None:
        self.dlg.ShowModal()
        self.dlg.Destroy()


class PcbQuotePlugin(pcbnew.ActionPlugin):
    def defaults(self):
        self.name = "PCB Quote"
        self.category = "Fabrication"
        self.description = ("Board size, Aisler estimate and links to PCB vendor "
                            "quote pages")
        self.show_toolbar_button = True

    def Run(self):
        import wx

        board = pcbnew.GetBoard()
        path = os.path.abspath(board.GetFileName()) if board else ""
        if not path:
            wx.MessageBox("Save the board first.", "PCB Quote", wx.ICON_INFORMATION)
            return
        width, height = _board_size_mm(board)
        estimate, error = _aisler_estimate(path)
        QuoteDialog(None, path, width, height, estimate, error).show()


PcbQuotePlugin().register()
