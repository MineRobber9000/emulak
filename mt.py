import core

mem = core.EmulakMemory()
cpu = core.EmulakCPU(mem)

prog = [0x0D,0x01,0x23,0x17,0x17,0x17,0x18,0x19,0x1A]

mem[0:len(prog)] = prog

cpu.setDebug(True)

for i in range(7):
	cpu.cycle()

cpu.printDebug()
