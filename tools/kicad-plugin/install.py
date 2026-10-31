#!/usr/bin/env python3
"""Install the PCB Quote API plugin into KiCad's user plugin folder.

    python3 tools/kicad-plugin/install.py

Restart KiCad afterwards (or use the refresh button on Preferences -> Action
Plugins). The action appears under Tools -> External Plugins -> PCB Quote and
as a toolbar button. KiCad creates an isolated Python environment for the
plugin and installs kicad-python (kipy) from requirements.txt on first run.
"""

from __future__ import annotations

import argparse
import os
import shutil
import sys
from pathlib import Path

FILES = ("__init__.py", "plugin.json", "quote.py", "requirements.txt")
LEGACY = ("action_plugin.py",)


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

    for name in LEGACY:
        stale = dest / name
        if stale.exists():
            stale.unlink()
            print(f"removed legacy {stale}")

    for name in FILES:
        shutil.copy2(src / name, dest / name)
        print(f"installed {name} -> {dest / name}")

    print("\nRestart KiCad (or click refresh on Preferences -> Action Plugins).")
    print("Then use Tools -> External Plugins -> PCB Quote.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
