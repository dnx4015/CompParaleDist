import sys,getopt
import subprocess as sub

RUN_TIMES = 20
def get_params(argv):
	target, threads = ("", "")
	try:
		opts, args = getopt.getopt(argv, "hf:t:", \
		["filename=", "nthreads="])
	except getopt.GetoptError:
		print  "run.py -f <filename> -t <numthreads>"
		sys.exit(2)
	for opt, arg in opts:
		if opt == "-h":
			print  "run.py -f <filename> -t <numthreads>"
			sys.exit()
		elif opt in ("-f", "--filename"):
			target = arg if arg[-4:] != ".cpp" else arg[:-4]
		elif opt in ("-t", "--nthreads"):
			threads = arg	
	return target, threads

def run(target, threads, first):
	if first:
		sub.check_output("make -f Makefile " + target, \
		stderr=sub.STDOUT, shell=True)
		sub.check_output("export OMP_NUM_THREADS=" + threads,\
		stderr=sub.STDOUT, shell=True)
	output = sub.check_output("./"+target+".out", \
	stderr=sub.STDOUT, shell=True)
	return output

def get_time(output):
	lines = output.split("\n");
	time = 0
	for i, line in enumerate(lines):
		if line[:4] == "Time":
			last = len(line)
			time=float(line[5:last-1])
	return time

def get_mean(target, threads):
	sum = 0.0
	for i in range(RUN_TIMES):
		sum += get_time(run(target, threads, i==0))
	return sum / float(RUN_TIMES)

def main(argv):
	target, threads = get_params(argv)
	target = target if target != "" else "../Code/mult"
	threads = (threads) if threads != "" else \
	("1", "2", "3", "4", "8", "16")
	for i, thread in enumerate(threads):
		print "Threads = "+thread
		print "Avg Time = "+str(get_mean(target, thread))

if __name__ == "__main__":
	main(sys.argv[1:])
