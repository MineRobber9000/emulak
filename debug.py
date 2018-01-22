import csv

breakpoints = []

class Breakpoint:
	def __init__(self,address,execute=True,read=False,write=False,jump=False):
		self.__dict__.update(locals())

def add_breakpoint(address,execute=True,read=False,write=False,jump=False):
	global breakpoints
	breakpoints.append(Breakpoint(address,execute,read,write,jump))

def get_breakpoints(type):
	global breakpoints
	return filter(lambda x: getattr(x,type),breakpoints)

def is_breakpoint(address,type):
	m = get_breakpoints(type)
	for b in m:
		if b.address == address:
			return True
	return False

def import_csv(bpf):
	global breakpoints
	with open(bpf) as f:
		r = csv.reader(f)
		r = list(r)
		r.pop(0)
		for l in r:
			b = Breakpoint(int(l[0],16))
			for k in l[1].split("+"):
				if hasattr(b,k):
					setattr(b,k,True)
			breakpoints.append(b)

#add_breakpoint(0x1234,jump=True)
