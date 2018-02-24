"""
Context Injection
CS 6120 Spring 2018
Author: Josh Miller
Credits:
 - NLTK, sklearn
 - Stanford CoreNLP CorefAnnotator
 - Sherin Thomas's python wrapper for Stanford CoreNLP CorefAnnotator
"""

import nltk
import numpy as np
from collections import defaultdict
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.stem.porter import PorterStemmer
import corenlp_pywrap as nlp

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

# sklearn tfidf
def train_tfidf(docs):
	tfidf = TfidfVectorizer(tokenizer=get_stems, stop_words='english')
	result = tfidf.fit_transform(docs)
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
	# TODO count coreferences of phrase in context
	raise NotImplementedError


def main():
	# hardcoded test data
	files = ["practice_data/train_data_1.txt", "practice_data/train_data_2.txt", "practice_data/train_data_3.txt"]
	texts = files_to_texts(files)
	docs = []
	for text in texts:
		docs.append(text)
	tfdict = train_tfidf(docs)
	print("done")


if __name__ == "__main__":
	main()
