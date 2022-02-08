"""
Course: CSE 251
Lesson Week: 05
File: team.py
Author: Brother Comeau

Purpose: Check for prime values

Instructions:

- You can't use thread/process pools
- Follow the graph in I-Learn 
- Start with PRIME_PROCESS_COUNT = 1, then once it works, increase it

"""
import time
import threading
import multiprocessing as mp
import random

#Include cse 251 common Python files
from cse251 import *
set_working_directory(__file__)

PRIME_PROCESS_COUNT = 1

def is_prime(n: int) -> bool:
    """Primality test using 6k+-1 optimization.
    From: https://en.wikipedia.org/wiki/Primality_test
    """
    if n <= 3:
        return n > 1
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i ** 2 <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

# TODO create read_thread function

def read_thread(filename, queue):
   with open(filename, 'r') as f:
        for line in f:
            queue.put(line)
        f.close()
        
# TODO create prime_process function

def is_prime(n: int) -> bool:
    if n <= 3:
        return n > 1
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i ** 2 <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

def prime_process(queue, primes):
    for i in queue:
        if is_prime(i):
            primes.put(i)

def create_data_txt(filename):
    with open(filename, 'w') as f:
        for _ in range(1000):
            f.write(str(random.randint(10000000000, 100000000000000)) + '\n')


def main():
    """ Main function """

    filename = 'data.txt'

    # Once the data file is created, you can comment out this line
    # create_data_txt(filename)

    log = Log(show_terminal=True)
    log.start_timer()

    # TODO Create shared data structures
    queue = mp.Queue()
    primes = mp.Manager().list([0] * 3)

    # TODO create reading thread
    read = threading.Thread(target=read_thread, args=(filename, queue))


    # TODO create prime processes

    pp1 = mp.Process(target=prime_process,args=(queue, primes,))
    pp2 = mp.Process(target=prime_process,args=(queue, primes,))
    pp3 = mp.Process(target=prime_process,args=(queue, primes,))

    # TODO Start them all
    read.start()
    read.join()

    # TODO wait for them to complete

    log.stop_timer(f'All primes have been found using {PRIME_PROCESS_COUNT} processes')

    # display the list of primes
    print(f'There are {len(primes)} found:')
    for prime in primes:
        print(prime)


if __name__ == '__main__':
    main()

