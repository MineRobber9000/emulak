# Emulak

A fantasy console in Python and Pygame. Currently a WIP.

## Lore

Emulak was released by a little-known company called Serix in early 1990. It was meant to be a competitor to the GameBoy. It featured
similar opcodes to that of the GameBoy's processor (both being based on the Z80) but it lacked VBlank interrupts and other similar
features. It contained a small keyboard (Editor's note: think flip-phone keyboard) that was memory-mapped, as well as a few other
registers. Due to how it was made, VRAM could be written to and read from at any time. Unfortunately for Serix, it was marketed poorly
and never sold as well as the other GameBoy competitors. It was so obscure that nobody even bothered to document it! Serix, after
facing the financial burden of the failure of the Emulak, filed for bankruptcy and quietly folded.

## How to use the Makefile

## Bonus

The way Emulak is implemented is also an FC! Simply subclass `game.BaseGame` and provide your own `init`, `update` and `draw` methods
and modify `main.py` to load your class instead of Emulak!
