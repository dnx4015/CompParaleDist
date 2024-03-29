import subprocess as sub
from aux import *

RUN_TIMES = 20

#EXECUTION OF PROGRAM
def run(target, threads, first):
	if first:
		sub.check_output("make -f Makefile " + target, \
		stderr=sub.STDOUT, shell=True)
		sub.check_output("export OMP_NUM_THREADS=" + threads,\
		stderr=sub.STDOUT, shell=True)
	output = sub.check_output("./"+target+".out", \
	stderr=sub.STDOUT, shell=True)
	return output

#GET OUTPUT OF EXECUTION
def get_time(output):
	lines = output.split("\n");
	time = 0.0
	for i, line in enumerate(lines):
		if line[:4] == "Time":
			last = len(line)
			time = float(line[5:last-1])
	return time

#GET AVERAGE TIME OF EXECUTION
def get_mean(target, threads):
	sum = 0.0
	for i in range(RUN_TIMES):
		sum += get_time(run(target, threads, i==0))
	return sum / float(RUN_TIMES)


def main(argv):
	directory, files, threads, output = get_params(argv)
	with open(output, "w") as f:
		for fin in get_files(directory, files):
			f.write(fin+"\n")
			for thread in get_threads(fin, threads):
				print "Processing file:",fin
				print "With # threads:", thread
				f.write(\
				"# threads: " + str(thread) + \
				", avg time: " + \
				str(get_mean(fin, thread))+"\n")

	


if __name__ == "__main__":
	main(sys.argv[1:])
