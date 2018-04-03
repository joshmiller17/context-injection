"""
Context Injection
CS 6120 Spring 2018
Author: Josh Miller
Credits: See README.md
"""
from __future__ import print_function
from __future__ import division

# init global args
args = None


# find subdirectories
def get_subdirs(dir):
	return [d for d in os.listdir(dir)
			if os.path.isdir(os.path.join(dir, d))]

# build the readability model using a directory of labeled text files
def build_readability_model():
	debug = args.debug
	read_dir = args.read
	verbose = args.verbose
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
	data, model, weights = readability.construct_readability_model(file_names, labels, verbose=args.verbose)
	
	print("INFO: Readability model constructed.")
	if verbose:
		readability.print_features(model)
			
	return model
	
	
	
# identifies a list of jargon terms using TFIDF
# returns list
def find_jargon_using_tfidf():
	input_doc = args.input
	background_dir = args.bg
	max_terms = args.maxterms
	stem = not args.nostem
	debug = args.debug
	tfidf_dictionary = tfidf.build_tfidf_model(background_dir, debug=args.debug, verbose=args.verbose, stem=(not args.nostem))
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
			if debug:
				print("--GOOD! Found a match.")
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
	
	# Make background dir into a .list file containing their names
	open("background.list", 'w').close()
	with open("background.list", 'a') as bg:
		for dirpath, dirnames, filenames in os.walk(background_dir):
				for file in filenames:
					if file.endswith(".txt"):
						bg.write(dirpath + "/" + file + "\n")
	
	
	cmd = []
	if not args.multi:
		cmd.append("The_Termolator/run_termolator_with_1_file_foreground.sh") # program
	else:
		cmd.append("The_Termolator/run_termolator.sh") # program
	cmd.append(args.input) # foreground
	cmd.append("background.list") # background
	cmd.append(".txt") # extension
	cmd.append(args.output) # output name
	cmd.append(str(not args.oldbg)) # if true, process background
	cmd.append(str(args.internet)) # use internet for relevance scoring
	cmd.append(str(args.allterms)) # considered terms
	cmd.append(str(args.maxterms)) # accepted terms
	cmd.append("The_Termolator") # directory of Termolator
	cmd.append("False") # "additional topic string", should always be false
	cmd.append(str(args.oldfg)) # if true skip preprocess foreground # TODO = args.oldfg
	cmd.append("False") # if false, use ranking.pkl
	
	print("INFO: executing command: " + ' '.join(cmd))
	call(cmd)
	
	termolator_jargon_terms = []
	# get files from generated terms file
	file_name = output_doc + ".out_term_list" 
	with open(file_name, 'r') as file:
		lines = file.readlines()
		for line in lines:
			words = line.split()
			termolator_jargon_terms.append(words[0])
	
	return termolator_jargon_terms

	
def main():
	# init sys args
	print("Successfully loaded.")
	input_doc = args.input
	output_doc = args.output
	read_dir = args.read
	background_dir = args.bg
	skip_read = args.noread
	skip_term = args.noterm
	skip_tfidf = args.notfidf
			
	# -----------------------------------
	# Build Models
	# -----------------------------------
	if read_dir != "" and read_dir != None and not skip_read:
		model = build_readability_model()
	elif not skip_read:
		# try to read from file: readability_model_weights.csv
		# = readability model saved when program last run
		# else if no file found, give warning that build must happen first
		try:
			model = joblib.load("readability_model.pkl", 'r')
		except Exception as e:
			print("ERROR: No readability model found on file. Please build readability model before continuing.")
			if debug:
				print("DEBUG: " + str(e))
			errors = True
			return errors
				
	if not skip_read:
		# future work? include topic density in the readability model?
	
		# calculate readability of document
		input_as_feature_vec = readability.feature_extraction([input_doc + ".txt"], verbose=args.verbose)
		prediction = readability.predict(model, input_as_feature_vec)
		print("Readability prediction:" + "\n" + str(prediction))
		open("read_output_" + input_doc + ".txt", 'w').close()
		with open("read_output_" + input_doc + ".txt", 'a') as file:
			file.write(str(prediction))
	
	
	# -----------------------------------
	# Find Jargon
	# -----------------------------------
	if background_dir:
	
		if not skip_tfidf:
			tfidf_jargon_terms = find_jargon_using_tfidf()
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
	import argparse
	prog_desc = "Input and output files assumed to be .txt, but do not include file extension." + \
			"Reads input from input file and analyzes jargon.\n" + \
			"Outputs jargon-identified text using TFIDF to output_tfidf.\n" + \
			"Outputs jargon-identified text using The Termolator to output_termolator.\n"
	epi = "Note that the directory of files for training the readability model is assumed to be split into several subdirectories." + \
			"\nWhen building the model, you will be prompted to give a readability value for each subdirectory, assumed to be a category representing one" + \
			"level of readability. The readability uses a scale of 1 (easy) to 100 (difficult).\n"
	parser = argparse.ArgumentParser(description=prog_desc, epilog=epi)
	parser.add_argument('-debug', action='store_true', help="Show debug info")
	parser.add_argument('-verbose', action='store_true', help="Show verbose output")
	parser.add_argument('-noread', action='store_true', help="Skip readability modeling")
	parser.add_argument('-notfidf', action='store_true', help="Skip TFIDF modeling")
	parser.add_argument('-noterm', action='store_true', help="Skip Termolator modeling")
	parser.add_argument('-nostem', action='store_true', help="Skip word-stemming for TFIDF")
	parser.add_argument('-maxterms', type=int, default=100, help="Max jargon terms accepted for Termolator and TFIDF")
	parser.add_argument('-allterms', type=int, default=1000, help="Max jargon terms considered for Termolator")
	parser.add_argument('-read', help="Directory for corpus that trains readability model. Can be left out if readability model was already built.")
	parser.add_argument('-bg', help="Directory for corpus that trains TFIDF and Termolator models")
	parser.add_argument('-oldbg', action='store_true', help="Background already processed (don't process again)")
	parser.add_argument('-oldfg', action='store_true', help="Foreground already processed (don't process again)")
	parser.add_argument('-multi', action='store_true', help="Input is a directory - finds jargon across all files")
	parser.add_argument('-internet', action='store_true', help="Use web for improved scoring (slow)")
	parser.add_argument('input', help="Input filename or directory")
	parser.add_argument('output', help="Output filename")
	
	args = parser.parse_args()
	
	if args.multi and not (args.noread and args.notfidf):
		parser.error("Multiple input files not implemented for readability and TFIDF. Please use -noread and -notfidf when using -multi.")
	
	if not (args.notfidf and args.noterm) and args.bg is None:
		parser.error("Background directory required to run TFIDF and Termolator.")

	# resolved later as needed
	#if not args.noread and args.read is None:
	#	parser.error("Readability directory required to run readability model.")
	
	if args.input.endswith(".txt") or args.output.endswith(".txt"):
		parser.error("Input and output filenames should not include file extensions.")
		
	print("\nLoading system operations...")
	import sys, os
	from sklearn.externals import joblib
	from subprocess import call

	print("\nLoading Context Injection...")
	import readability
	import tfidf
	import define

	errcode = main()
	if not errcode:
		print("Finished successfully.")
	else:
		print("Exited with errors.")