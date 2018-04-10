# Crawl wikipedia to get categories for each article in the database

from queue import Queue
from threading import Thread
import time
import threading
import requests
from bs4 import BeautifulSoup


def crawl(book):
    url = 'https://en.wikibooks.org' + str(book)
    # print("Scraping :", url)
    source_code = requests.get(url)  # Get the source code of the web-page
    plain_text = source_code.text  # Get all the text from the source code

    bsobj = BeautifulSoup(plain_text, "html.parser")  # Create a BeautifulSoup object
    main = bsobj.findAll('div', {'class': 'mw-normal-catlinks'})[0]

    # print([x.get('href') for x in main.findAll('a')])
    category = main.findAll('a')[1].get('href')
    # print("CATEGORY: ", category)
    return category


def crawler(book):
    prev_cat = ""
    stop = '/wiki/Category:Subject:Books_by_subject'
    while book != stop:
        # print(book)
        prev_cat = book
        book = crawl(book)

    else:
        return prev_cat.split(":")[-1]


def thread_test(book, id):
    # csvf = open("books_by_category.csv", "a", encoding="utf-8")
    if id % 100 == 0:
        print("Read {} books...".format(id))
    book = book[:-1].split(":")[-1]
    book_wiki = "/wiki/" + book
    # print(book_wiki)
    # print("Categorizing ", book)
    with open("books_by_category.csv", "a", encoding="utf-8") as csvf:
        try:
            category = crawler(book_wiki)
            # print(book, ":", category, "| threading.activeCount()", threading.activeCount())
            csvf.write("{0},{1},{2}\n".format(id, book, category))
        except Exception:
            pass
        # print("Skipping ", book)


class DownloadWorker(Thread):
    def __init__(self, queue):
        Thread.__init__(self)
        self.queue = queue

    def run(self):
        while True:
            # Get the work from the queue and expand the tuple
            book, id = self.queue.get()
            thread_test(book, id)
            self.queue.task_done()


def main():
    ts = time.time()
    f = open("enwikibooks-20180220-pages-articles-multistream-index.txt", "r", encoding="utf-8")
    books = f.readlines()
    f.close()
    books = books[47126:]
    # Create a queue to communicate with the worker threads
    # print(books)
    queue = Queue()
    # Create 8 worker threads
    for x in range(8):
        worker = DownloadWorker(queue)
        # Setting daemon to True will let the main thread exit even though the workers are blocking
        worker.daemon = True
        worker.start()
    # Put the tasks into the queue as a tuple
    for id, book in enumerate(books):
        id = id + 47126
        # logger.info('Queueing {}'.format(book))
        queue.put((book, id))
    # Causes the main thread to wait for the queue to finish processing all the tasks
    queue.join()
    print('Took {}'.format(time.time() - ts))


if __name__ == '__main__':
    main()
