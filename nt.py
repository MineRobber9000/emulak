import core,main

game = core.Emulak(main.ScreenControl(),["-d"])

last_pc = 0x1234

while game.memory.pc!=last_pc:
#	last_pc = game.memory.pc
	game.update([])
	game.draw()
	game.draw()

game.cpu.printDebug()
