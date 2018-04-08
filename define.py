"""
Context Injection
CS 6120 Spring 2018
Author: Dave Lowell
Credits: See README.md
"""

from __future__ import print_function
from __future__ import division
print("\nReading Wikipedia...\n")
import wikipedia as wiki
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from collections import defaultdict
import string
import argparse
import os
import readability
from sklearn.externals import joblib

try:
	stopwords = stopwords.words('english')
	stopwords.extend(list(string.punctuation))
except LookupError:
	print("INFO: stopwords not found, downloading now")
	nltk.download('stopwords')
	stopwords = stopwords.words('english')
	stopwords.extend(list(string.punctuation))



#could improve by intelligently selecting the number of sentences to use
#could improve by intelligently disambiguating when multiple results are available
def define(query, summary_length=2, debug=False):
	try:
		#retrieve text information from wikipedia article
		article = wiki.page(query)
		sentences = sent_tokenize(article.summary)
		text = [word_tokenize(sent.lower()) for sent in sentences]
		text = [[word for word in sent if word not in stopwords] \
				for sent in text]
		#calculate initial word weights (probabilities)
		num_words = 0
		word_weights = defaultdict(int)
		for sent in text:
			num_words += len(sent)
			for word in sent:
				word_weights[word] += 1
		for word in word_weights.keys():
			word_weights[word] = word_weights[word]/num_words

		summary = []
		#choose sentence i to add to the summary
		def select(i):
			summary.append(sentences.pop(i))
			for word in text[i]:
				word_weights[word] = word_weights[word]**2
			text.pop(i)

		#we start with the first sentence, as this introduces the topic
		select(0)
		while len(summary) < summary_length and len(sentences) > 0:
			#select the topic word that the next sentence must contain
			best_word, _ = max(word_weights.items(), key=lambda x: x[1])
			best_sentence = -1
			best_score = 0
			#find the best sentence
			for i, sent in enumerate(text):
				if best_word not in sent:
					continue
				else:
					score = 0
					for word in sent:
						score += word_weights[word]
					score = score/len(sent)
					if score > best_score:
						best_score = score
						best_sentence = i
			#update the summary and weights
			select(best_sentence)
		if debug:
			print("TRACE: summary for " + query + " is: " + ' '.join(summary))
		return summary
		
		#return wiki.summary(query, sentences=sentences)
	except wiki.exceptions.DisambiguationError as e:
		return define(e.options[0])
	except wiki.exceptions.PageError as e:
		#do something
		return 'no definition found'
	except:
		return 'unknown error'

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('input', help="Directory of files of jargons to define.")
	parser.add_argument('-verbose', help="Verbose output.")
	parser.add_argument('-read', action='store_true', help="Calculate readability of each definition.")
	args = parser.parse_args()
	
	if args.read:
		try:
			model = joblib.load("readability_model.pkl", 'r')
		except Exception as e:
			print("ERROR: No readability model found on file. Please build readability model before continuing.")
			exit(1)
			

	for dirpath, dirnames, filenames in os.walk(args.input):
		for file in filenames:
			if file.endswith(".txt") and not file.startswith("defined_"):
				with open(os.path.join(dirpath,file), 'r') as f:
					print("Reading " + str(file) + "...")
					jargons = f.readlines()
					open(os.path.join(dirpath,"defined_" + file), 'w').close()
					with open(os.path.join(dirpath,"defined_" + file), 'w') as jf:
						for jargon in jargons:
							jf.write("\n\n")
							jf.write(str(jargon) + " is defined as: ")
							definition = define(jargon)
							definition = ' '.join(definition) # collapse across sentences
							try:
								definition = definition.decode('utf-8', 'ignore').encode('ascii', 'ignore')
							except:
								print("problem happen")
								continue
							jf.write(definition + '\n')
							if args.read:
								print("Analyzing this definition:")
								print(definition)
								print("For this jargon:")
								print(jargon)
								def_input = [definition]
								input_as_feature_vec = readability.feature_extraction(def_input, verbose=args.verbose, text_only=True)
								prediction = readability.predict(model, input_as_feature_vec)
								print("Readability prediction:" + "\n" + str(prediction))
								open(os.path.join(dirpath,jargon + "_read_score.txt"), 'w').close()
								with open(os.path.join(dirpath,jargon + "_read_score.txt"), 'a') as file:
									file.write(str(prediction))
	print("Done.")