# Hand-solder J3 (relay socket)

J3 is **excluded from every provider assembly BOM/CPL**. It is the 2.54 mm
1×3 right-angle socket for the KY-019 relay module, and it has to be raised so
its opening meets the relay module's male header. Automated through-hole
assembly places parts flush to the board and cannot hold a part on a spacer,
so this one socket is hand-fitted.

## Why a flush socket does not work

The relay module's 3-pin header sits above its PCB. In the 3D model the header
pins are at about **3.7–4.1 mm above the board**, while a standard right-angle
socket mounted flush has its opening lower. Fitted flush, the relay header
does not seat. The 3D model also shows the relay lying flat for visualisation;
physically it stands in the right-angle socket, so do not use the model's Z as
the build height.

## What to fit

- 2.54 mm 1×3 **right-angle female header with long pins**, e.g. LCSC
  **C54876732** (`PM2.54-1x3PWZ-H8.5`) or another long-pin right-angle 1×3.
- A long-pin part lets you raise the socket body and still reach the board;
  trim the pins underneath after soldering.
- The board's J3 pads are at `(44, 69)`, `(44, 71.54)` and `(44, 74.08)` mm,
  with pad 1 nearest the board's bottom edge.

## Procedure

1. Order the board with J3 **unpopulated** (the assembly BOM/CPL already omit it).
2. Plug the KY-019 relay's 3-pin header into the socket.
3. Dry-fit the relay in its intended position (screw terminals facing the
   wiring side) and lower/raise the socket until the relay header seats and
   the relay body sits as planned. Expect roughly **1–1.5 mm of raise** as a
   starting point; measure the actual relay and socket.
4. Solder the three pins to the J3 pads, keeping the socket square to the board
   and at the height set in step 3. Trim the long pins flush underneath.
5. Check that the relay inserts and removes without straining the socket or
   the board, and that the screw terminals remain accessible.

## If a provider supports custom THT spacing

Some assembly houses accept a non-flush through-hole part if you supply a
placement note. In that case the instruction is: *fit J3 at the height that
mates with the KY-019 module (about 1–1.5 mm above flush), using a long-pin
right-angle 1×3 socket; do not press the body flush to the board.* Most
low-cost services do not offer this, hence the exclusion.
