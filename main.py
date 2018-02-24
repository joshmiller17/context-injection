"""
Context Injection
CS 6120 Spring 2018
Author: Josh Miller
Credits:
 - NLTK, sklearn
 - Stanford CoreNLP CorefAnnotator
 - Sherin Thomas's python wrapper for Stanford CoreNLP CorefAnnotator
"""

import readability
import tfidf


def train_model(data, labels):
    model = sklearn.linear_model.LinearRegression(normalize=True)
    model.fit(data, labels)
    return model  # can get weights from model.get_params


def predict(model, datum):
    return model.predict(datum)

def main():
	
	print("done")


if __name__ == "__main__":
	main()
