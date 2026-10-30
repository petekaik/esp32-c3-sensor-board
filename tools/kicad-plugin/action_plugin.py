"""KiCad action plugin: Aisler price estimate for the open board.

Install: copy this directory to
    macOS   ~/Documents/KiCad/10.0/scripting/plugins/aisler-quote/
    Linux   ~/.local/share/kicad/10.0/scripting/plugins/aisler-quote/
then restart KiCad and enable it in PCB Editor -> Tools -> External Plugins.

It shells out to ../../../tools/aisler_quote.py (resolved from this file) so the
pricing logic lives in one place and is also usable from the command line.
"""

from __future__ import annotations

import os
import subprocess
import sys

import pcbnew  # noqa: F401  (provided by KiCad)


class AislerQuotePlugin(pcbnew.ActionPlugin):
    def defaults(self):
        self.name = "Aisler Quote"
        self.category = "Fabrication"
        self.description = "Estimate Aisler PCB price for the current board"
        self.show_toolbar_button = True

    def Run(self):
        import wx

        board = pcbnew.GetBoard()
        path = board.GetFileName() if board else ""
        if not path:
            wx.MessageBox("Save the board first.", "Aisler Quote", wx.ICON_INFORMATION)
            return

        script = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
            "tools", "aisler_quote.py",
        )
        if not os.path.exists(script):
            wx.MessageBox(f"Quote script not found:\n{script}", "Aisler Quote", wx.ICON_ERROR)
            return

        lines = []
        for qty in (3, 5, 10):
            try:
                out = subprocess.run(
                    [sys.executable, script, "--pcb", path, "--qty", str(qty)],
                    capture_output=True, text=True, timeout=30,
                )
                lines.append(out.stdout.strip() or out.stderr.strip())
            except Exception as exc:              # pragma: no cover - GUI path
                lines.append(f"{qty} pcs: {exc}")

        wx.MessageBox(
            "\n\n".join(lines) + "\n\nPrices use Aisler's published Budget formula "
            "(job fee + area x fee x qty), not a live quote.",
            "Aisler Quote", wx.ICON_INFORMATION,
        )


AislerQuotePlugin().register()
