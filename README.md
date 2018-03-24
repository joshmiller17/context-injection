# Creating the Database:

Get the WikiDump:

`wget https://dumps.wikimedia.org/enwikibooks/latest/enwikibooks-latest-pages-articles-multistream.xml.bz2`

`enwikibooks-20180220-pages-articles-multistream-index.txt` contains title of each fetched article.

Run the following to extract text from xml dumps:

`python WikiExtractor.py -cb 250K -o extracted enwikibooks-latest-pages-articles-multistream.xml.bz2`

Run `python multithreaded_get_categories.py` to get the categories for each fetched article. 

`books_by_category.csv` contains each article mapped with its category.

Open the preprocess.ipynb to store each cleaned article into seperate directories with their categories as titles. 

<hr>  

