"""A script to make adding examples easier."""
import sys,os.path

def unpack(t):
	return t[0],t[1],t[2:]

script,filename,args = unpack(sys.argv)

if filename == "start":
	with open("Makefile","w") as f:
		f.write("all: {}\n".format(" ".join(args)))
	sys.exit(0)

name,ext = os.path.splitext(filename)

with open("Makefile","a") as f:
	f.write("\n")
	f.write("{0}.bin: {0}.{1}\n".format(name,ext))
	f.write("\txxd -p -r {0}.{1} > {0}.bin\n".format(name,ext))
