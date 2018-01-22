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

Run `make` to make an instruction list from `list.txt` (use when you've made a new opcode and added it to the list)

Run `make test` to run a test using a program. (The test ends when the program enters an infinite loop to the same address)

Run `make debug` to start Emulak in debug mode.

Run `make examples` to make the examples (binary files in `examples/`)

## Bonus

The way Emulak is implemented is also an FC! Simply subclass `game.BaseGame` and provide your own `init`, `update` and `draw` methods
and modify `main.py` to load your class instead of Emulak!
