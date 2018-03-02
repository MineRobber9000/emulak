from __future__ import print_function
from game import BaseGame
from collections import OrderedDict
import debug as d
import sys
from pygame.locals import *

def center(c,d):
	return (d-c)/2

def myhex(n,a=False):
	if a:
		return hex(n)[2:].zfill(4)
	return hex(n)[2:].zfill(2)

def getgrayscalef(n):
	return (255./n)

def getgrayscale(s,v):
	n = int(round(s*((v-97)+1)))
	return (n,n,n)

#s = getgrayscalef(26)
#gsp = [getgrayscale(s,v) for v in range(122,98,-1)]
#black = len(gsp)-1
#red = len(gsp)
#gsp.append((255,0,0))
gsp = [(0,0,0),(255,0,0),(0,255,0),(0,0,255),(255,255,255)][::-1]
black = 4
red = 3
green = 2
blue = 1
white = 0

class EmulakMemory:
	def __init__(self,s=65535):
		self.memory = [0]*s
		self.pc = 0

	def loadProg(self,prog,entrypoint=0x6000):
		self.memory[entrypoint:entrypoint+len(prog)]=prog
		self.pc = entrypoint
#		print(myhex(entrypoint+prog.index(0x0d)))

	def getProgByte(self):
		ret = self.memory[self.pc]
		self.pc+=1
#		print(myhex(ret))
		return ret

	def setByte(self,i,v):
		self.memory[i]=v

	def getByte(self,i):
		return self.memory[i]

	def __getitem__(self,k):
		return self.getByte(k)

	def __setitem__(self,k,v):
		self.setByte(k,v)

class EmulakStack:
	def __init__(self):
		self.addresses = []

	def push(self,v):
		self.addresses.append(v)

	def pop(self):
		return self.addresses.pop()

	def __getitem__(self,k):
		return self.addresses[k]

	def __setitem__(self,k,v):
		return # no need to worry about this yet, but here's the implementation so I don't have to write it later
#		self.addresses[k]=v

class EmulakCPU:
	def __init__(self,memory):
		self.memory = memory
		self.stack = EmulakStack()
		self.debug = False
		self.breakpoints = False
		self.registers = OrderedDict(a=0,b=0,c=0,d=0,e=0,f=0,h=0,l=0)
		d.import_csv("breakpoints.csv")
		self.opcodes = dict()
		self.gopcode = 0
		self.defineOpcode(self.nop)
		self.defineOpcode(self.absJump)
		self.defineOpcode(self.absCall)
		self.defineOpcode(self.returnFromCall)
		self.defineOpcode(self.loadA)
		self.defineOpcode(self.loadB)
		self.defineOpcode(self.loadC)
		self.defineOpcode(self.loadD)
		self.defineOpcode(self.loadE)
		self.defineOpcode(self.loadH)
		self.defineOpcode(self.loadL)
		self.defineOpcode(self.loadBC)
		self.defineOpcode(self.loadDE)
		self.defineOpcode(self.loadHL)
		self.defineOpcode(self.loadAIndirect)
		self.defineOpcode(self.loadBIndirect)
		self.defineOpcode(self.loadCIndirect)
		self.defineOpcode(self.loadDIndirect)
		self.defineOpcode(self.loadEIndirect)
		self.defineOpcode(self.loadHIndirect)
		self.defineOpcode(self.loadLIndirect)
		self.defineOpcode(self.storeA)
		self.defineOpcode(self.pushBC)
		self.defineOpcode(self.pushDE)
		self.defineOpcode(self.pushHL)
		self.defineOpcode(self.popBC)
		self.defineOpcode(self.popDE)
		self.defineOpcode(self.popHL)
		self.defineOpcode(self.increaseA)
		self.defineOpcode(self.subtract)

	def printDebug(self):
		print("PC: $"+(hex(self.memory.pc)[2:].zfill(4)))
#		print(hex(self.memory[0x0003])[2:].zfill(2).upper())
		for i in list("abcdefhl"):
			print("{}: {}".format(i.upper(),hex(self.registers[i])[2:].zfill(2).upper()),end=" ")
		print()
		if len(self.stack.addresses):
			print(",".join(["$"+(hex(x)[2:].zfill(4)) for x in self.stack.addresses]))

	def register(self,r,v=None):
		if v:
			if r in self.registers and r!="f": # seperate 8-bit registers (16-bit registers use this under the hood)
				self.registers[r]=(v%256)
			elif r=="(hl)": # indirect hl
				self.memory[self.resolveAddress([self.registers["h"],self.registers["l"]])]=(v%256)
		else:
			if r in self.registers and r!="f":
				return self.registers[r]
			elif r in ("bc","de","hl","af"):
				return self.resolveAddress([self.registers[r[0]],self.registers[r[1]]])
			elif r=="(hl)":
				return self.memory[self.resolveAddress([self.registers["h"],self.registers["l"]])]

	def defineOpcode(self,f):
		self.opcodes[self.gopcode]=f
		self.gopcode+=1

	def setBreakpoints(self,bp):
		self.breakpoints = bp

	def setDebug(self,b):
		self.debug = b
		self.setBreakpoints(b)

	def triggerBreakpoint(self,a=0,push=False,cycled=False):
		if not cycled:
			self.memory.pc-=1
		if push:
			self.stack.push(a)
		print("-"*48)
		print("Breakpoint triggered!")
		self.printDebug()
		print("-"*48)
		sys.exit(0)

	def resolveAddress(self,bs):
		bs = [myhex(i) for i in bs]
		bs = "".join(bs)
#		print(bs)
		return int(bs,16)

	def nop(self):
		return

	def absJump(self):
		address = []
		for i in range(2):
			address.append(self.memory.getProgByte())
		address = address[::-1]
#		address = [hex(i)[2:].zfill(2) for i in address]
#		address = "".join(address)
		if self.debug or self.breakpoints:
			if d.is_breakpoint(self.resolveAddress(address),"jump"):
				self.triggerBreakpoint(self.resolveAddress(address)) # address we were going to jump to
		self.memory.pc=self.resolveAddress(address)

	def absCall(self):
		self.stack.push(self.memory.pc)
		self.absJump()

	def returnFromCall(self):
		a = self.stack.pop()
		if self.debug or self.breakpoints:
			if d.is_breakpoint(a,"jump"):
				self.triggerBreakpoint(a,True) # address we were going to jump to, push it (it's a return)
		self.memory.pc=a

	def loadreg(self,r,a=False):
		if a:
			address = [self.memory.getProgByte() for i in range(2)]
			address = address[::-1]
			address = self.resolveAddress(address)
			#print(address)
			self.register(r,self.memory[address])
		else:
			self.register(r,self.memory.getProgByte())

	def loadreg16(self,r):
		self.loadreg(r[0])
		self.loadreg(r[1])

	"""Immediate load A"""
	def loadA(self):
		self.loadreg("a")

	"""Immediate load B"""
	def loadB(self):
		self.loadreg("b")

	"""Immediate load C"""
	def loadC(self):
		self.loadreg("c")

	"""Immediate load D"""
	def loadD(self):
		self.loadreg("d")

	"""Immediate load E"""
	def loadE(self):
		self.loadreg("e")

	"""Immediate load H"""
	def loadH(self):
		self.loadreg("h")

	"""Immediate load L"""
	def loadL(self):
		self.loadreg("l")

	"""Immediate load BC"""
	def loadBC(self):
		self.loadreg16("bc")

	"""Immediate load DE"""
	def loadDE(self):
		self.loadreg16("de")

	"""Immediate load HL"""
	def loadHL(self):
		self.loadreg16("hl")

	"""Indirect load A"""
	def loadAIndirect(self):
		self.loadreg("a",True)

	"""Indirect load B"""
	def loadBIndirect(self):
		self.loadreg("b",True)

	"""Indirect load C"""
	def loadCIndirect(self):
		self.loadreg("c",True)

	"""Indirect load D"""
	def loadDIndirect(self):
		self.loadreg("d",True)

	"""Indirect load E"""
	def loadEIndirect(self):
		self.loadreg("e",True)

	"""Indirect load H"""
	def loadHIndirect(self):
		self.loadreg("h",True)

	"""Indirect load L"""
	def loadLIndirect(self):
		self.loadreg("l",True)

	def storeA(self):
		a = self.register("a")
		address = [self.memory.getProgByte() for i in range(2)]
		address = address[::-1]
		address = self.resolveAddress(address)
		self.memory[address]=a

	def pushreg16(self,r):
		self.stack.push(self.register(r[0])*0x100+self.register(r[1]))

	def popreg16(self,r):
		v = self.stack.pop()
		self.register(r[0],v/0x100)
		self.register(r[1],v%0x100)

	def pushBC(self):
		self.pushreg16("bc")

	def pushDE(self):
		self.pushreg16("de")

	def pushHL(self):
		self.pushreg16("hl")

	def popBC(self):
		self.popreg16("bc")

	def popDE(self):
		self.popreg16("de")

	def popHL(self):
		self.popreg16("hl")

	def increase(self,ra,address=False):
		if address:
			self.memory[ra]+=1
		else:
			self.registers[ra]+=1

	def increaseA(self):
		self.increase("a")

	def subtract(self):
		self.register("a",self.register("a")-self.memory.getProgByte())

	def cycle(self):
		if self.breakpoints:
			if d.is_breakpoint(self.memory.pc,"execute"):
				self.triggerBreakpoint(None,False,True) # no address, don't push, is an execute breakpoint
		if self.debug:
			self.printDebug()
		opcode = self.memory.getProgByte()
		if self.debug:
			print(self.opcodes[opcode].func_name)
		self.opcodes[opcode]()

def m(l):
	if len(l)>1:
		return l[0]*m(l[1:])
	else:
		return l[0]*1

def xy(c,r):
	return (c%r[0],c/r[0])

class Emulak(BaseGame):

	SCALE_FACTOR = 16

	# We need the empty ticks for a semblance of HW speed, so Emulak.EMPTY_TICKS = True
	EMPTY_TICKS = True

	def resolution(self):
		return (480/self.SCALE_FACTOR,320/self.SCALE_FACTOR)

	def tickVRAM(self):
		for i in range(m(self.resolution())):
			c = self.memory[0xCA7F+i]
			c = c & len(gsp)
#			print(i,c)
			try:
				self.plotPixel(xy(i,self.resolution()),gsp[c])
			except IndexError as e:
				self.plotPixel(xy(i,self.resolution()),(255,255,255))


	"""Initialize variables"""
	def init(self):
		self.ms = self.screencontrol.newSurface(480,320)
	#	print(self.resolution())
		self.ms.fill((255,255,255))
		#self.font = self.screencontrol.getFont("Arial")
		self.delayframes = 0
		#self.delayframes = 60
		self.screencontrol.setTitle("Emulak")
		self.memory = EmulakMemory()
		self.memory[0xCA7F]=black
#		self.memory[0xCA7F+1]=red
#		self.memory[0xCA7F+2]=black
		with open("input.bin","rb") as f:
			self.memory.loadProg(map(ord,f.read()))
		#self.memory.pc = 24576
		self.cpu = EmulakCPU(self.memory)
		# handle arguments
		self.ap.add_argument("--debug","-d",action="store_true",help="Shows debug information. Implies -b.")
		self.ap.add_argument("--breakpoints","-b",action="store_true",help="Stops the emulator when a breakpoint is triggered.")

	def handleArguments(self):
		if self.args.debug:
			self.cpu.setDebug(self.args.debug)
		if self.args.breakpoints:
			self.cpu.setBreakpoints(self.args.breakpoints)

	def plotPixel(self,l,c):
		l = [n*self.SCALE_FACTOR for n in l]
	#	l = list(l)
		for yn in range(self.SCALE_FACTOR):
			for xn in range(self.SCALE_FACTOR):
				self.ms.set_at((l[0]+xn,l[1]+yn),c)

	"""Called every update frame (every other frame)"""
	def update(self,events):
		for event in events:
			if event.type==KEYDOWN:
				self.memory[0x0000] = event.key
		self.cpu.cycle()
		if self.memory[0x0001]!=0:
			if self.memory[0x0002]==1:
				self.delayframes=self.memory[0x0001]
				self.memory[0x0002]=0
#		if self.memory[0x0003]!=0 and (self.memory[0x0003]>=97 and self.memory[0x0003]<=122):
#			self.plotPixel((2,0),gsp[self.memory[0x0003]-97])
#			self.memory[0x0003]=0
		return

	"""Called every frame."""
	def draw(self):
		if self.delayframes:
			self.delayframes-=1
			self.memory[0x0001]=self.delayframes
			return
		self.tickVRAM()
		self.screencontrol.fill((128,128,128))
		self.screencontrol.blitSurface(self.ms,center(480,self.screencontrol.size[0]),center(320,self.screencontrol.size[1]))
		self.screencontrol.finishDraw()
