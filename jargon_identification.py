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
    print(ret)
    print(tfidf.get_feature_names()) # TODO remove print statements


def get_tfidf(tfidf, word):
    token = nltk.word_tokenize(word)
    stem = PorterStemmer().stem(token)
    # TODO return value of tfidf(stem) from tfidf matrix


def count_coreferences(phrase, context):
    # TODO count coreferences of phrase in context
    return


def main():
    # TODO import corpus
    # TODO stem corpus
    # TODO test tfidf
    return


if __name__ == "__main__":
    main()
