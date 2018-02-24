"""
Context Injection
CS 6120 Spring 2018
Author: Josh Miller
Credits:
 - NLTK, sklearn
 - Stanford CoreNLP CorefAnnotator
 - askmyhat's python wrapper for Stanford CoreNLP CorefAnnotator
"""

import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.stem.porter import PorterStemmer
import stanford_corenlp_python_wrapper as nlp

def files_to_texts(files):
	texts = []
	for i in range(len(files)):
		file = files[i]
		text = (open(file, 'r')).read
		texts.append(text)
	return texts

# nltk stemmer
def get_stems(input):
	tokenized = nltk.word_tokenize(input)
	stems = []
	for token in tokenized:
		stems.append(PorterStemmer().stem(token))
	return stems


# sklearn tfidf
def train_tfidf(stems):
	tfidf = TfidfVectorizer(tokenizer=get_stems, stop_words='english')
	ret = tfidf.fit_transform(stems.values())
	print "RET:\n", ret
	print "TFIDF features:\n", tfidf.get_feature_names() # TODO remove print statements
	print "TFIDF full:\n", tfidf

def get_tfidf(tfidf, word):
	token = nltk.word_tokenize(word)
	stem = PorterStemmer().stem(token)
	# TODO return value of tfidf(stem) from tfidf matrix


def count_coreferences(phrase, context):
	# TODO count coreferences of phrase in context
	return


def main():
	# hardcoded test data
	files = ["practice_data/train_data_1.txt", "practice_data/train_data_2.txt", "practice_data/train_data_3.txt"]
	texts = files_to_texts(files)
	stems = []
	for text in texts:
		stems.extend(get_stems(text))
	model = train_tfidf(stems)
	print "done"


if __name__ == "__main__":
	main()
