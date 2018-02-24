"""
Context Injection
CS 6120 Spring 2018
Author: Josh Miller
"""
import sklearn
import nltk
import string
import numpy
from nltk.tokenize import sent_tokenize
from nltk.corpus import cmudict

# import re

"""
FEATURES [by index]
[0] total paragraphs
[1] total sentences
[2] total words
[3] total syllables
[4] avg sent/para
[5] avg word/sent
[6] avg syl/word
[7] complex words (syl > 2) / total words
[8] very complex words (syl > 3) / total words
[9] difficult words (not in dale-chall) / total words
[10] filler words / total words
[11] hedge words / total words
[12] weasel words / total words
[13] simple american words / total words
"""


# input: data as a list of file names
# output: feature vector for each data point
def feature_extraction(data):
    print("\nExtracting features on " + str(len(data)) + " file(s)")

    # preparation stuff
    try:
        dictionary = cmudict.dict()
    except LookupError:
        print("INFO: cmudict not found, downloading now")
        nltk.download('cmudict')
        dictionary = cmudict.dict()

    # read in dictionaries of special words
    with open("special_words/dale_chall_words.txt", 'r') as dc:
        dale_chall = dc.readlines()
    with open("special_words/filler_words.txt", 'r') as fill:
        filler = fill.readlines()
    with open("special_words/hedge_words.txt", 'r') as h:
        hedge = h.readlines()
    with open("special_words/simple_words.txt", 'r') as s:
        simple = s.readlines()
    with open("special_words/weasel_words.txt", 'r') as w:
        weasel = w.readlines()

    # init feature matrix; will be size len(data) x 14, since there are 14 features
    features = [[0 for i in range(15)] for j in range(len(data))]

    for i in range(len(data)):
        file = data[i]
        text = (open(file, 'r')).read()
        paragraphs = text.split('\n')
        total_sentences = 0
        total_words = 0
        total_syllables = 0
        complex_words = 0
        very_complex_words = 0
        total_hedges = 0
        total_weasels = 0
        total_simple = 0
        total_difficult = 0
        total_filler = 0
		total_special_char = 0

        for paragraph in paragraphs:
            try:
                sentences = sent_tokenize(paragraph)
            except LookupError:
                print("INFO: punkt not found, downloading now")
                nltk.download('punkt')
                sentences = sent_tokenize(paragraph)

            num_sentences = len(sentences)
            total_sentences += num_sentences
            for sentence in sentences:
                words = nltk.word_tokenize(sentence)
                num_words = len(words)
                total_words += num_words
                for word in words:
                    try:
                        num_syllables = max(
                            [len([y for y in x if (y[-1]) in string.digits]) for x in dictionary[word.lower()]])
                    except KeyError:
                        # attempt to guess at number of syllables without dictionary
                        if len(word) < 5:
                            acronym = True
                            for char in word:
								if not char.isalnum():
									total_special_char += 1
                                if char.islower():
                                    acronym = False
                            if acronym:
                                num_syllables = len(word)
                            else:
                                num_syllables = 1
                        else:
                            guess_1 = 1 + len(word) / 3  # an educated guess
                            guess_2 = 1 + len(word) % 3  # a lucky guess
                            num_syllables = (guess_1 + guess_2) / 2
                    if num_syllables < 1 or num_syllables > 10:
                        print "Warning: Syllable count for", word, "is", num_syllables 
                        print "Proceeding anyway..." 
                    total_syllables += num_syllables
                    if num_syllables > 2:
                        complex_words += 1
                        if num_syllables > 3:
                            very_complex_words += 1
                    if word not in dale_chall:
                        total_difficult += 1
                    if word in filler:
                        total_filler += 1
                    if word in simple:
                        total_simple += 1
                    if word in hedge:
                        total_hedges += 1
                    if word in weasel:
                        total_weasels += 1

        features[i][0] = len(paragraphs)
        features[i][1] = total_sentences
        features[i][2] = total_words
        features[i][3] = total_syllables
        features[i][4] = total_sentences / len(paragraphs)
        features[i][5] = total_words / total_sentences
        features[i][6] = total_syllables / total_words
        features[i][7] = complex_words / total_words
        features[i][8] = very_complex_words / total_words
        features[i][9] = total_difficult / total_words
        features[i][10] = total_filler / total_words
        features[i][11] = total_hedges / total_words
        features[i][12] = total_weasels / total_words
        features[i][13] = total_simple / total_words
		features[i][14] = total_special_char / total_words

    return features


def main():
    # hardcoded test data
    texts = ["practice_data/train_data_1.txt", "practice_data/train_data_2.txt", "practice_data/train_data_3.txt"]
    labels = [2, 6, 12]
    data = feature_extraction(texts)
    model = train_model(data, labels)
    weights = model.coef_
    features = ["[0] total paragraphs",
                "[1] total sentences", "[2] total words", "[3] total syllables", "[4] avg sent/para",
                "[5] avg word/sent",
                "[6] avg syl/word", "[7] complex words (syl > 2) / total words",
                "[8] very complex words (syl > 3) / total words",
                "[9] difficult words (not in dale-chall) / total words",
                "[10] filler words / total words", "[11] hedge words / total words",
                "[12] weasel words / total words", "[13] simple american words / total words",
				"[14] total special chars / total words"]
    for i in range(15):
        print(features[i], " = ", weights[i])
        continue
    test_data = feature_extraction(["practice_data/test.txt"])
    print("Predicted readability score:", model.predict(test_data))


if __name__ == "__main__":
    main()
