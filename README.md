# context-injection
An NLP project for text simplification through context injection.
Main features:
* Fits and tests a readability model (linear regression) to determine readability of a target document
* Finds jargon phrases using TFIDF
* Finds jargon phrases using The Termolator

# Credits and Acknowledgements

Project authors: Josh Miller, Aniruddha Tapas, Dave Lowell

Data for special words (Dale-Chall, filler words, hedge words, simple American-English words, and weasel words) from https://github.com/words
Code for syllable counting from user aks on StackOverflow (see "To find the number of syllables in a word").
Implementation of The Termolator from https://github.com/AdamMeyers/The_Termolator
Other notable libraries used: nltk, sklearn, numpy.
