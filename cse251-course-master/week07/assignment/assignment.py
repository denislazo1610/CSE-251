"""
Course: CSE 251
Lesson Week: 07
File: assingnment.py
Author: <Your name here>
Purpose: Process Task Files
Instructions:  See I-Learn
TODO
Add you comments here on the pool sizes that you used for your assignment and
why they were the best choices.
"""

from datetime import datetime, timedelta
import requests
import multiprocessing as mp
from matplotlib.pylab import plt
import numpy as np
import glob
import math 

# Include cse 251 common Python files - Dont change
from cse251 import *
set_working_directory(__file__)

TYPE_PRIME  = 'prime'
TYPE_WORD   = 'word'
TYPE_UPPER  = 'upper'
TYPE_SUM    = 'sum'
TYPE_NAME   = 'name'

# Global lists to collect the task results
result_primes = []
result_words = []
result_upper = []
result_sums = []
result_names = []

def is_prime(n: int):
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
 
def task_prime(value):
    """
    Use the is_prime() above
    Add the following to the global list:
        {value} is prime
            - or -
        {value} is not prime
    """
    if is_prime(value):
        return f'{value} is prime'
    else:
        return f'{value} is not prime'

    pass

def task_word(word):
    """
    search in file 'words.txt'
    Add the following to the global list:
        {word} Found
            - or -
        {word} not found *****
    """
    with open('words.txt') as f:
        if word in f.read():
            return f'{word} Found'
        else:
            return f'{word} not found'
           
    pass 

def task_upper(text):
    """
    Add the following to the global list:
        {text} ==>  uppercase version of {text}
    """
    text = text.upper()
    return text
    pass

def task_sum(start_value, end_value):
    """
    Add the following to the global list:
        sum of {start_value:,} to {end_value:,} = {total:,}
    """
    sum = 0
    for i in range(start_value, end_value):
        sum += i

    return sum
    pass

def task_name(url):
    """
    use requests module
    Add the following to the global list:
        {url} has name <name>
            - or -
        {url} had an error receiving the information
    """
    info = requests.get(url)
    info = info.json()
    string = f'{url} has name {info["name"]}'
    return string
    pass


def main():
    log = Log(show_terminal=True)
    log.start_timer()

    # TODO Create process pools
    poolPrime = mp.Pool(1)
    poolWord = mp.Pool(1)
    poolUpper = mp.Pool(1)
    poolSum = mp.Pool(1)
    poolName = mp.Pool(1)

    count = 0
    task_files = glob.glob("*.task")
    for filename in task_files:
        # print()
        # print(filename)
        task = load_json_file(filename)
        print(task)
        count += 1
        task_type = task['task']
        
        if task_type == TYPE_PRIME:
            poolPrime.apply_async(task_prime, args = {task['value'],}, callback = lambda x: result_primes.append(x))
            # task_prime(task['value'])
        elif task_type == TYPE_WORD:
            poolWord.apply_async(task_word, args = {task['word'],}, callback = lambda x: result_words.append(x))
            # task_word(task['word'])
        elif task_type == TYPE_UPPER:
            poolUpper.apply_async(task_upper, args = {task['text'],}, callback = lambda x: result_upper.append(x))
            # task_upper(task['text'])
        elif task_type == TYPE_SUM:
            poolSum.apply_async(task_sum, args = {task['start'],task['end']}, callback = lambda x: result_sums.append(x))
            # task_sum(task['start'], task['end'])
        elif task_type == TYPE_NAME:
            poolName.apply_async(task_name, args = {task['url'],}, callback = lambda x: result_names.append(x))
            # task_name(task['url'])
        else:
            log.write(f'Error: unknown task type {task_type}')

    # TODO start and wait pools

    poolPrime.close()
    poolWord.close()
    poolUpper.close()
    poolSum.close()
    poolName.close()

    poolPrime.join()
    poolWord.join()
    poolUpper.join()
    poolSum.join()
    poolName.join()


    # Do not change the following code (to the end of the main function)
    def log_list(lst, log):
        for item in lst:
            log.write(item)
        log.write(' ')
    
    log.write('-' * 80)
    log.write(f'Primes: {len(result_primes)}')
    log_list(result_primes, log)

    log.write('-' * 80)
    log.write(f'Words: {len(result_words)}')
    log_list(result_words, log)

    log.write('-' * 80)
    log.write(f'Uppercase: {len(result_upper)}')
    log_list(result_upper, log)

    log.write('-' * 80)
    log.write(f'Sums: {len(result_sums)}')
    log_list(result_sums, log)

    log.write('-' * 80)
    log.write(f'Names: {len(result_names)}')
    log_list(result_names, log)

    log.write(f'Primes: {len(result_primes)}')
    log.write(f'Words: {len(result_words)}')
    log.write(f'Uppercase: {len(result_upper)}')
    log.write(f'Sums: {len(result_sums)}')
    log.write(f'Names: {len(result_names)}')
    log.stop_timer(f'Finished processes {count} tasks')

if __name__ == '__main__':
    main()