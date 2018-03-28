"""
Context Injection
CS 6120 Spring 2018
Author: Josh Miller
Credits: See README.md
"""

from __future__ import print_function
import nltk
import numpy as np
import os
from readability import pre_process
from collections import defaultdict
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.stem.porter import PorterStemmer
#import corenlp_pywrap as nlp


def files_to_texts(files):
	texts = []
	for i in range(len(files)):
		file = files[i]
		text = (open(file, 'r')).read()
		texts.append(text)
	return texts

# nltk stemmer
def get_stems(input):
	try:
		tokenized = nltk.word_tokenize(input)
	except LookupError:
		print("INFO: punkt not found, downloading now")
		nltk.download("punkt")
		tokenized = nltk.word_tokenize(input)
	stems = []
	for token in tokenized:
		stems.append(stem(token))
	return stems

def stem(token):
	return PorterStemmer().stem(token)
	
def no_stem_tokenizer(input):
	try:
		tokenized = nltk.word_tokenize(input)
	except LookupError:
		print("INFO: punkt not found, downloading now")
		nltk.download("punkt")
		tokenized = nltk.word_tokenize(input)
	return tokenized


# sklearn tfidf
def train_tfidf(docs, stem=True, verbose=False):
	if len(docs) < 1:
		print("ERROR: No documents to train TFIDF on")
		return None
	if verbose:
		print("INFO: pre-processing " + str(len(docs)) + " documents.")
	processed_docs = []
	for doc in docs:
		clean = pre_process(doc)
		processed_docs.append(clean)
	if verbose:
		print("INFO: Training TFIDF model, stemming set to " + str(stem))
	print("INFO: Training TFIDF Vectorizer...")
	if stem:
		tfidf = TfidfVectorizer(tokenizer=get_stems, stop_words='english')
	else:
		tfidf = TfidfVectorizer(tokenizer=no_stem_tokenizer, stop_words='english')
	result = tfidf.fit_transform(processed_docs)
	scores = zip(tfidf.get_feature_names(), np.asarray(result.sum(axis=0)).ravel())
	tfdict = defaultdict(float)
	for score in scores:
		tfdict[score[0]] = score[1]
	
	return tfdict
	
	
def get_tfidf(tfdict, word):
	token = nltk.word_tokenize(word)
	stem = stem(token)
	return tfdict[stem]


def count_coreferences(phrase, context):
	# future work? count coreferences of phrase in context
	raise NotImplementedError
	

def train_model(data, labels):
	model = sklearn.linear_model.LinearRegression(normalize=True)
	model.fit(data, labels)
	
	return model  # can get weights from model.get_params


def predict(model, datum):
	return model.predict(datum)

	
# future work? use joblib to save and load models
# input: directory of files
# output: tfidf dictionary
def build_tfidf_model(background_dir, file=False, debug=False, verbose=False, stem=True):
	if debug:
		print("DEBUG: Building TFIDF model, stem=" + str(stem))
	files = []
	if file:
		files = [background_dir + ".txt"]
	else:
		for dirpath, dirnames, filenames in os.walk(background_dir):
			for file in filenames:
				files.append(os.path.join(dirpath, file))
		if debug:
			print(str(len(files)) + " files found in background " + background_dir)
			if len(files) < 10:
				for f in files:
					print(f)
	texts = files_to_texts(files)
	if len(texts) < len(files):
		print("ERROR: Some files were unable to be processed. " + len(texts) + " / " + len(files))
	tfdict = train_tfidf(texts, verbose=verbose, stem=stem)
	return tfdict
	
	
def main():
	# hardcoded test data
	files = ["practice_data/train_data_1.txt", "practice_data/train_data_2.txt", "practice_data/train_data_3.txt"]
	texts = files_to_texts(files)
	tfdict = train_tfidf(texts)
	print("done")


if __name__ == "__main__":
	main()
