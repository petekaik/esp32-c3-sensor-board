#!/usr/bin/env python3
"""Install the PCB Quote action plugin into KiCad's user plugin folder.

    python3 tools/kicad-plugin/install.py
    python3 tools/kicad-plugin/install.py --dest ~/Documents/KiCad/10.0/scripting/plugins

Restart KiCad afterwards; the plugin appears under
Tools -> External Plugins -> PCB Quote and as a toolbar button.
"""

from __future__ import annotations

import argparse
import os
import shutil
import sys
from pathlib import Path

FILES = ("action_plugin.py", "plugin.json")


def default_dest() -> Path:
    home = Path.home()
    if sys.platform == "darwin":
        return home / "Documents" / "KiCad" / "10.0" / "scripting" / "plugins"
    if os.name == "nt":
        return Path(os.environ.get("APPDATA", home)) / "kicad" / "10.0" / "scripting" / "plugins"
    return home / ".local" / "share" / "kicad" / "10.0" / "scripting" / "plugins"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--dest", help="KiCad scripting/plugins directory")
    ap.add_argument("--name", default="pcb-quote", help="plugin folder name")
    args = ap.parse_args()

    src = Path(__file__).resolve().parent
    dest_root = Path(args.dest).expanduser() if args.dest else default_dest()
    dest = dest_root / args.name
    dest.mkdir(parents=True, exist_ok=True)

    for name in FILES:
        shutil.copy2(src / name, dest / name)
        print(f"installed {name} -> {dest / name}")

    print("\nRestart KiCad, then Tools -> External Plugins -> PCB Quote.")
    print("If the toolbar button is hidden: Preferences -> PCB Editor -> "
          "Show external plugin toolbar.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
