# Explanations

 - `test.xxd` - Recieves keyboard input
 - `pushhl.xxd` - Loads HL with a value and makes sure that pushing an address to the stack works
 - `increasea.xxd` - Increases A every cycle. Loops infinitely.
 - `indirectjump1.xxd` - Uses stack pushing to indirectly jump to $1234.
 - `gradient.xxd` - Allows one to affect the screen (Testing for VRAM features) by pressing letter buttons. NOTICE: this example is deprecated and requires a previous version of Emulak to work.
 - `cycle.xxd` - cycles through the palette

Run `make` to make the whole batch. Move the one you want to try to `input.bin` in the same directory as `main.py` and the other
Emulak files. Alternatively, run `make examples` in the top-level directory of Emulak to make these.
