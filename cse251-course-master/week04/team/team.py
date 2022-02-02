"""
Course: CSE 251
Lesson Week: 04
File: team.py
Author: Brother Comeau

Purpose: Team Activity

Instructions:

- See in I-Learn

"""

import threading
import queue
import requests
import json

# Include cse 251 common Python files
from cse251 import *
set_working_directory(__file__)

RETRIEVE_THREADS = 1        # Number of retrieve_threads
NO_MORE_VALUES = 'No more'  # Special value to indicate no more items in the queue

def retrieve_thread(q,log):  # TODO add arguments
    """ Process values from the data_queue """

    while True:
        # TODO check to see if anything is in the queue
        while(q[0]):
        # TODO process the value retrieved from the queue

        # TODO make Internet call to get characters name and log it
            log.write('name')


def file_reader(q,log): # TODO add arguments
    """ This thread reading the data file and places the values in the data_queue """

    # TODO Open the data file "data.txt" and place items into a queue
    file1 = open("data.txt", 'r')
    lines = file1.readlines()

    for line in lines:
        q.put(line)

    log.write('finished reading file')

    # TODO signal the retrieve threads one more time that there are "no more values"



def main():
    """ Main function """

    log = Log(show_terminal=True)

    # TODO create queue
    q = queue.Queue()
    # TODO create semaphore (if needed)

    # TODO create the threads. 1 filereader() and RETRIEVE_THREADS retrieve_thread()s
    # Pass any arguments to these thread need to do their job
    reader = threading.Thread(target=file_reader, args={q,log})
    retriever = threading.Thread(target=retrieve_thread, args={q,log})


    log.start_timer()

    # TODO Get them going - start the retrieve_threads first, then file_reader
    retriever.start()
    reader.start()
    

    # TODO Wait for them to finish - The order doesn't matter

    reader.join()
    retriever.join()

    log.stop_timer('Time to process all URLS')


if __name__ == '__main__':
    main()




