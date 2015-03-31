from pylab import *

def read_content(fpath):
	data = [{}] * 100
	names = []
	times = []
	i = 0;
	with open(fpath) as f:
		content = f.readlines()
	for line in content:
		if line[:2] == "..":
			if i < 4:
				data[i] = {'name':line[15:-1], 'threads':{}}
			else:
				data[i] = {'name':line[33:-1]+'CO', 'threads':{}}
			i+=1
		elif line[0] == "#":
			pos = line.find(":")
			posEnd = line.find(",")
			n = int(line[pos+2:posEnd])
			pos = line.find(":", posEnd)
			time = float(line[pos+2:])
			data[i-1]['threads'][n] = time
			names.append(data[i-1]['name']+", "+str(n))
			times.append(time)
	return names, times

def make_plot(names, times):
	figure(1)
	x = range(len(names))
	xticks(x, names)
	plot(x, times, 'g')
	xlabel('Tests')
	ylabel('Time(s)')
	savefig('../Doc/Images/test.pdf')

if __name__ == "__main__":
	n,t = read_content("../Results/all.txt")
	print n,t
	#make_plot(n,t)
