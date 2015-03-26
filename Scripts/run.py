import sys,getopt
import subprocess as sub

RUN_TIMES = 20
def get_params(argv):
	target, threads = ("", "")
	try:
		opts, args = getopt.getopt(argv, "hf:t:", \
		["filename=", "nthreads="])
	except getopt.GetoptError:
		print  "To run all experimets just execute:\n\
		python run.py\n\
		To run an exact file or number of threads execute:\n\
		python run.py -f <filename> -t <numthreads>"
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
	targets, threads = get_params(argv)
	targets = targets if targets != "" else \
	("../Code/multSeq", "../Code/multParalleli", \
	"../Code/multParallelj", ".../Code/multParallelk")
	threads = (threads) if threads != "" else \
	("1", "2", "3", "4", "8", "16")
	with open("../Results/experiments.txt", "w") as f:
		for target in targets:
			f.write(target[8:-4]+"\n")
			t_threads = "1" if target[12:-4] == "Seq" else threads
			for thread in t_threads:
				f.write("# threads: "+str(thread)+", avg time: "\
				+str(get_mean(target, thread))+"\n")

	


if __name__ == "__main__":
	main(sys.argv[1:])
