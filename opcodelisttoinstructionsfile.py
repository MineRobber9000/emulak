import copy
def myhex(n):
	return "0x"+hex(n)[2:].zfill(2)

opcodes = []
with open("list.txt") as f:
	opcodes = [l.strip() for l in f]
out = dict()
for i in range(256):
	if i<len(opcodes):
		out[myhex(i)] = opcodes[i]
	else:
		out[myhex(i)] = "JAM"
with open("instructions.txt","w") as f:
	ks = copy.copy(out.keys())
	ks.sort()
	for k in ks:
		f.write("{} - {}\n".format(k,out[k]))
