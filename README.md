# Context-Injection
An NLP project for text simplification through context injection.
Main features:
* Fits and tests a readability model (linear regression) to determine readability of a target document
* Finds jargon phrases using TFIDF
* Finds jargon phrases using The Termolator

# Details:
* Input and output files assumed to be .txt, but do not include file extension. 
* Reads input from input file and analyzes jargon.
* Outputs jargon-identified text using TFIDF to output_tfidf.
* Outputs jargon-identified text using The Termolator to output_termolator.
* The directory of files for training the readability model is assumed to be split into several subdirectories.
* When building the model, you will be prompted to give a readability value for each subdirectory, assumed to be a category representing one level of readability. The readability uses a scale of 1 (easy) to 100 (difficult).

## Usage
The script is invoked with an input text file and an output text file as arguments. 

Sample: `python main.py -notfidf -noterm james_joyce_test_input out`

The readability of this input novel will be outputted in a file named `read_output_james_joyce_test_input.txt`


    usage: main.py [-h] [-debug] [-verbose] [-noread] [-notfidf] [-noterm]
               	   [-nostem] [-maxterms MAXTERMS] [-allterms ALLTERMS]
               	   [-read READ] [-bg BG] [-oldbg] [-oldfg] [-multi] [-internet]
                   input output

    positional arguments:
	  input               Input filename or directory
	  output              Output filename

    optional arguments:
	  -h, --help          Show this help message and exit
	  -debug              Show debug info
	  -verbose            Show verbose output
	  -noread             Skip readability modeling
	  -notfidf            Skip TFIDF modeling
	  -noterm             Skip Termolator modeling
	  -nostem             Skip word-stemming for TFIDF
	  -maxterms MAXTERMS  Max jargon terms accepted for Termolator and TFIDF
	  -allterms ALLTERMS  Max jargon terms considered for Termolator
	  -read READ          Directory for corpus that trains readability model. Can
			      be left out if readability model was already built.
	  -bg BG              Directory for corpus that trains TFIDF and Termolator
			      models
	  -oldbg              Background already processed (don't process again)
	  -oldfg              Foreground already processed (don't process again)
	  -multi              Input is a directory - finds jargon across all files
	  -internet           Use web for improved scoring (slow)


# Credits and Acknowledgements

Project authors: Josh Miller, Dave Lowell, Aniruddha Tapas 

* Data for special words (Dale-Chall, filler words, hedge words, simple American-English words, and weasel words) from https://github.com/words
* Code for syllable counting from user aks on StackOverflow (see [To find the number of syllables in a word](https://stackoverflow.com/questions/5087493/to-find-the-number-of-syllables-in-a-word)).
* Implementation of The Termolator from https://github.com/AdamMeyers/The_Termolator
* [WikiExtractor.py](http://medialab.di.unipi.it/wiki/Wikipedia_Extractor) to extract and clean text from a [Wikipedia database dump](http://download.wikimedia.org/).

Libraries used: nltk, sklearn, numpy.

<hr>
