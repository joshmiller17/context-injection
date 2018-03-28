"""
Context Injection
CS 6120 Spring 2018
Author: Josh Miller
Credits: See README.md
"""
from __future__ import print_function
from __future__ import division

print("\nLoading system operations...")
import sys, os
from sklearn.externals import joblib
from subprocess import call

print("\nLoading Context Injection...")
import readability
import tfidf
import define

# TODO look into having multiple files all importing same thing - efficiency?

# init global vars
verbose = False
debug = False


# find subdirectories
def get_subdirs(dir):
	return [d for d in os.listdir(dir)
			if os.path.isdir(os.path.join(dir, d))]

# build the readability model using a directory of labeled text files
def build_readability_model(read_dir):
	global verbose, debug
	file_count = 0
	file_names = []
	subdirs = get_subdirs(read_dir)
	if not subdirs:
		print("ERROR: no subdirectories found in " + read_dir)
		return None
	elif debug:
		print("DEBUG: list of subdirectories is ", subdirs)
	labels = []
	for category in subdirs:
		label = -1
		while label < 1 or label > 100:
			label = input("Please input a readability value for " + category + " from 1 (easy) to 100 (difficult)\n  >")
		
		for file in os.listdir(os.path.join(read_dir, category)):
			path = os.path.join(read_dir, category)
			if file.endswith(".txt"):
				file_names.append(os.path.join(path, file))
				labels.append(label)
			else:
				if debug:
					print("DEBUG: " + file + " is not a .txt file")
				
	assert len(labels) == len(file_names)
	data, model, weights = readability.construct_readability_model(file_names, labels, verbose=verbose)
	
	print("INFO: Readability model constructed.")
	if verbose:
		readability.print_features(model)
			
	return model
	
	
	
# identifies a list of jargon terms using TFIDF
# returns list
def find_jargon_using_tfidf(input_doc, background_dir, max_terms=None, stem=True):
	global verbose, debug
	tfidf_dictionary = tfidf.build_tfidf_model("../" + background_dir, debug=debug, verbose=verbose, stem=stem) # for some reason, Termolator needs background dir to be higher
	if tfidf_dictionary is None:
		return None
	# find suitable cutoff point if none given
	file = open(input_doc + '.txt', 'r')
	file_size = len(file.read())
	if debug:
		print("DEBUG: input file size is", file_size)
	if max_terms is None:
		max_terms = min(5, int(round(file_size / 1000)) + 1)
	if debug:
		print("DEBUG: Using at most", max_terms, "terms for TFIDF model.")
	file.close()
	input_dict = tfidf.build_tfidf_model(input_doc, file=True)
	if input_dict is None:
		return None
	
	jargon_dict = {} # saved as dict for debugging
	for word in input_dict:
		if debug:
			print("TRACE: input jargon found - " + word + " " + str(input_dict[word]))
		if word in tfidf_dictionary:
			jargon_dict[word] = tfidf_dictionary[word]
		elif debug:
			print("...No matching jargon in background; discarding.")
	
	jargon_sorted = []
	terms_remaining = int(max_terms)
	if debug:
		print("DEBUG: TFIDF scores for chosen jargon terms")
	for word, score in sorted(jargon_dict.iteritems(), key=lambda (key,val): (val,key)):
		if terms_remaining < 1:
			break
		if debug:
			print("    ", word, "    =    ", score)
		jargon_sorted.append(word)
		terms_remaining -= 1

	return jargon_sorted
	
	
# identifies a list of jargon terms using The Termolator
# saves results to output_termolator.txt
def find_jargon_using_termolator(input_doc, background_dir, output_doc):
	global verbose, debug
	
	# Make background dir into a .list file containing their names
	open("background.list", 'w').close()
	with open("background.list", 'a') as bg:
		for dirpath, dirnames, filenames in os.walk("../" + background_dir):
				for file in filenames:
					if file.endswith(".txt"):
						bg.write( dirpath + "/" + file + "\n")
	
	cmd = []
	cmd.append("The_Termolator/run_termolator_with_1_file_foreground.sh") # program
	cmd.append(input_doc) # foreground
	cmd.append("background.list") # background
	cmd.append(".txt") # extension
	cmd.append(output_doc) # output name
	cmd.append("True") # don't process background files
	cmd.append("False") # use internet for relevance scoring
	cmd.append("1000") # considered terms
	cmd.append("100") # accepted terms
	cmd.append("The_Termolator") # directory of Termolator
	cmd.append("False") # additional topic string
	cmd.append("False") 
	cmd.append("False") 
	cmd.append("False") 
	
	print("INFO: executing command: " + ' '.join(cmd))
	call(cmd)
	
	termolator_jargon_terms = []
	# get files from generated terms file
	file_name = output_doc + ".all_terms" 
	with open(file_name, 'r') as file:
		lines = file.readlines()
		for line in lines:
			words = line.split()
			termolator_jargon_terms.append(words[0])
	
	return termolator_jargon_terms

	
def main():
	global verbose, debug
	# init sys args
	print("Successfully loaded.")
	input_doc = ""
	output_doc = ""
	read_dir = ""
	background_dir = ""
	errors = False
	HELP = "\nUsage: main.py [options] input output\n" + \
			"Input and output files assumed to be .txt\n" + \
			"Reads input from input file and analyzes jargon.\n" + \
			"Outputs jargon-identified text using TFIDF to output_tfidf.\n" + \
			"Outputs jargon-identified text using The Termolator to output_termolator.\n" + \
			"    Options:\n" + \
			"        --help             Show usage, then exit\n" + \
			"        --debug            Debug output\n" + \
			"        -v                 Verbose output\n" + \
			"        -noread            Skip readability modeling\n" + \
			"        -notfidf           Skip TFIDF modeling\n" + \
			"        -noterm            Skip Termolator modeling\n" + \
			"        -nostem            Don't stem words when doing TFIDF\n" + \
			"        -maxterms m        Set max jargon terms used for TFIDF model" + \
			"        -read dir          Build readability model from files in directory dir.\n" + \
			"        -background dir    Set the background corpus for training jargon models.\n" + \
			"If no background is given, the program uses a known background or throws an error if none exists.\n" + \
			"The directory of files for training the readability model is assumed to be split into several subdirectories." + \
			"\nWhen building the model, you will be prompted to give a readability value for each subdirectory, assumed to be a category representing one" + \
			"level of readability. The readability uses a scale of 1 (easy) to 100 (difficult).\n"
			
	skip = False
	unk_arg = False
	help = False
	skip_read = False
	skip_tfidf = False
	skip_term = False
	max_terms = None
	do_stem = True
	for a in range(len(sys.argv)):
		if skip == True:
			skip = False
			continue
		else:
			if sys.argv[a].endswith(".py"):
				continue
			if sys.argv[a][0] == '-': #option
				if sys.argv[a] == '--help':
					print(HELP)
					help = True
					return help
				elif sys.argv[a] == '--debug':
					debug = True
				elif sys.argv[a] == '-v':
					verbose = True
				elif sys.argv[a] == '-noread':
					skip_read = True
				elif sys.argv[a] == '-notfidf':
					skip_tfidf = True
				elif sys.argv[a] == '-noterm':
					skip_term = True
				elif sys.argv[a] == '-nostem':
					do_stem = False
				elif sys.argv[a] == '-maxterms':
					skip = True
					max_terms = sys.argv[a+1]
				elif sys.argv[a] == '-read':
					skip = True
					read_dir = sys.argv[a+1]
				elif sys.argv[a] == '-background':
					skip = True
					background_dir = sys.argv[a+1]
				else:
					unk_arg = True
			elif not skip:
				if "." in sys.argv[a]:
					errors = True
					print("ERROR: File names should not include extensions.")
					return errors
				if input_doc != "":
					if output_doc != "":
						print("ERROR: Multiple input/output documents detected: " + input_doc + " and " + output_doc + " and " + sys.argv[a])
						print("Type --help for usage.")
						errors = True
						return errors
					else:
						output_doc = sys.argv[a]
				else:
					input_doc = sys.argv[a]
			
	if unk_arg:
		errors = True
		print("One or more unknown options. Type --help for usage.")

	if input_doc == "" and not errors:
		errors = True
		print("No input document recognized. Type --help for usage.")
	if output_doc == "" and not errors:
		errors = True
		print("No output document recognized. Type --help for usage.")
		
	if errors:
		print("Exiting due to command errors.")
		return errors
			
	# -----------------------------------
	# Build Models
	# -----------------------------------
	if read_dir != "" and not skip_read:
		model = build_readability_model(read_dir)
	elif not skip_read:
		# try to read from file: readability_model_weights.csv
		# = readability model saved when program last run
		# else if no file found, give warning that build must happen first
		try:
			read_model = joblib.load("readability_model.pkl", 'r')
		except Exception as e:
			print("ERROR: No readability model found on file. Please build readability model before continuing.")
			if debug:
				print("DEBUG: " + str(e))
			errors = True
			return errors
				
	if not skip_read:
		# future work? include topic density in the readability model?
	
		# calculate readability of document
		input_as_feature_vec = readability.feature_extraction([input_doc + ".txt"], verbose=verbose)
		prediction = readability.predict(read_model, input_as_feature_vec)
		print("Readability prediction:" + "\n" + str(prediction))
		open("read_output_" + input_doc + ".txt", 'w').close()
		with open("read_output_" + input_doc + ".txt", 'a') as file:
			file.write(str(prediction))
	
	
	# -----------------------------------
	# Find Jargon
	# -----------------------------------
	if background_dir:
	
		if not skip_tfidf:
			tfidf_jargon_terms = find_jargon_using_tfidf(input_doc, background_dir, max_terms = max_terms, stem = do_stem)
			open("tfidf_output_" + input_doc + ".txt", 'w').close()
			with open("tfidf_output_" + input_doc + ".txt", 'a') as file:
				for j in tfidf_jargon_terms:
					file.write(str(j) + "\n")
		
		if not skip_term:
			termolator_jargon_terms = find_jargon_using_termolator(input_doc, background_dir, output_doc)
			
			
			# TODO context injection using the termolator's list of jargon
			# TODO save as [input_doc]_injected.txt
			#if not skip read
			#	input_as_feature_vec = readability.feature_extraction([input_doc + "_injected.txt"], verbose=verbose)
			#	prediction = readability.predict(read_model, input_as_feature_vec)
			#	print("New readability with context injected: " + str(prediction))

		open("overlapping_jargon_" + input_doc + ".txt", 'w').close()
		with open("overlapping_jargon_" + input_doc + ".txt", 'a') as file:
				
			if not (skip_tfidf or skip_term):
				for tf_jargon in tfidf_jargon_terms:
					for term_jargon in termolator_jargon_terms:
						match = True
						for ch in range(len(tf_jargon)):
							if tf_jargon[ch] != term_jargon:
								match = False
						if match:
							file.write(term_jargon + "\n")
		
		
	return errors

if __name__ == "__main__":
	errcode = main()
	if not errcode:
		print("Done.")