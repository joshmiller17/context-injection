# Creating the Database:

Download the preprocessed database from [here](https://drive.google.com/a/husky.neu.edu/file/d/1bPI-PPxW417Rhj_61dkbCr1OP4ozfVbx/view?usp=drive_web).

Get the WikiDump:

`wget https://dumps.wikimedia.org/enwikibooks/latest/enwikibooks-20180220-pages-articles-multistream.xml.bz2`

`enwikibooks-20180220-pages-articles-multistream-index.txt` contains title of each fetched article.

Run the following to extract text from xml dumps:

`python WikiExtractor.py --file -o extracted enwikibooks-20180220-pages-articles-multistream.xml`

Run `python multithreaded_get_categories.py` to get the categories for each fetched article. 

`books_by_category/books_by_category.csv` and `books_by_category/books_by_category2.csv` contains each article mapped with its category.

Open and run the `get_data.ipynb` to merge the categorized titles into an index file called `allbooks_by_category.csv` and also prepare the Database directory

Open and run the `clean_data.ipynb` to store each cleaned article into seperate directories with their categories as titles. 

<hr>

Similar procedure can be followed to get the simplewikibooks data (Compressed to the `simplewikibooks.zip`).

<hr>
