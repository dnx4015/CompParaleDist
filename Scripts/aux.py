import sys,getopt
from os import walk

#DEFAULT VALUES
DEFAULT_DIR = ("../Code/")
DEFAULT_FILE = ""
DEFAULT_THREADS = ("1", "2", "3", "4", "8", "16")
DEFAULT_OUT = "../Results/all.txt"

HELP =  "All the programs in the Code directory are execute by:\n\
		python run.py\n\
		To run all files in a specific path use:\n\
		python run.py -p <path> or --path <path>\n\
		To run an exact file use:\n\
		python run.py -f <filename> or --file <filename>\n\
		To run an exact number of threads use:\n\
		python run.py -t <num_threads> --nthreads <num_threads>\
		\n\n\
		All results are output into the Results directory\n\
		To output the results to one file use:\n\
		python run.py -o <filename> --output <filename>"


#GETALL FILES FROM DIRECTORY
def get_files(path, files):
	if files != "":
		return files
	f = []
	for (dirpath, dirnames, filenames) in walk(path):
		f.extend([dirpath+"/"+fin[:-4] for fin in filenames \
		if fin[-4:] == ".cpp"])
	return f


#PARAMETERS EXTRACTION
def get_params(argv):
	directory = DEFAULT_DIR
	files = DEFAULT_FILE
	threads = DEFAULT_THREADS
	output = DEFAULT_OUT
	try:
		opts, args = getopt.getopt(argv, "hp:f:t:o:", \
		["path=","file=", "nthreads=", "output="])
	except getopt.GetoptError:
		print HELP
		sys.exit(2)
	for opt, arg in opts:
		if opt == "-h":
			print HELP
			sys.exit()
		elif opt in ("-p", "--path"):
			directory = arg 
		elif opt in ("-f", "--file"):
			files = arg if arg[-4:] != ".cpp" else arg[:-4]
		elif opt in ("-t", "--nthreads"):
			threads = arg
		elif opt in ("-o", "--output"):
			output = arg

	return directory, files, threads, output

#HACK SEQ FILE
get_threads = lambda name, default:\
("1") if "Seq" in name else default 

