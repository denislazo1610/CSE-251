"""
Course: CSE 251
Lesson Week: 10
File: assignment.py
Author: <your name>

Purpose: assignment for week 10 - reader writer problem

Instructions:

- Review TODO comments

- writer: a process that will send numbers to the reader.  
  The values sent to the readers will be in consecutive order starting
  at value 1.  Each writer will use all of the sharedList buffer area
  (ie., BUFFER_SIZE memory positions)

- reader: a process that receive numbers sent by the writer.  The reader will
  accept values until indicated by the writer that there are no more values to
  process.  
  
- Display the numbers received by the reader printing them to the console.

- Create WRITERS writer processes

- Create READERS reader processes

- You can use sleep() statements for any process.

- You are able (should) to use lock(s) and semaphores(s).  When using locks, you can't
  use the arguments "block=False" or "timeout".  Your goal is to make your
  program as parallel as you can.  Over use of lock(s) or lock(s) in the wrong
  place will slow down your code.

- You must use ShareableList between the two processes.  This shareable list
  will contain different "sections".  There can only be one shareable list used
  between your processes.
  1) BUFFER_SIZE number of positions for data transfer. This buffer area must
     act like a queue - First In First Out.
  2) current value used by writers for consecutive order of values to send
  3) Any indexes that the processes need to keep track of the data queue
  4) Any other values you need for the assignment

- Not allowed to use Queue(), Pipe(), List() or any other data structure.

- Not allowed to use Value() or Array() or any other shared data type from 
  the multiprocessing package.

Add any comments for me:



"""
from multiprocessing import Semaphore, shared_memory
import random
from multiprocessing.managers import SharedMemoryManager
import multiprocessing as mp

BUFFER_SIZE = 10
READERS = 2
WRITERS = 2
def send_info(shared, start, end, sempahoreToAdd, semaphoreToTake):
  
  for i in range(start, end):
    # print(sempahoreToAdd) 
    sempahoreToAdd.acquire()
    for x in range(0, 10):
      if shared[x] == 0:
        shared[x] = i
        semaphoreToTake.release()
        # print(shared)
        break;


  return 0

def receiving_info(shared, sempahoreToAdd, semaphoreToTake):
  while True:

    for x in range(0, 10):
      semaphoreToTake.acquire()
      if shared[x] != 0:
        print(f'{shared[x]} value received')
        shared[x] = 0
        sempahoreToAdd.release()



def main():

    # This is the number of values that the writer will send to the reader
    # items_to_send = random.randint(1000, 10000)
    items_to_send = 20



    smm = SharedMemoryManager()
    smm.start()

    # TODO - Create a ShareableList to be used between the processes

    sharedList = shared_memory.ShareableList([0] * BUFFER_SIZE)
    # print(sharedList)
   


    # TODO - Create any lock(s) or semaphore(s) that you feel you need
    full = Semaphore(10)
    
    empty = Semaphore(0)

    # TODO - create reader and writer processes

    writer = mp.Process(target=send_info, args=(sharedList, 1, items_to_send + 1, full, empty))
    reader = mp.Process(target=receiving_info, args=(sharedList, full, empty ))

    # TODO - Start the processes and wait for them to finish

    writer.start()
    reader.start()


    writer.join()
    reader.join()

    print(f'{items_to_send} values sent')


    # for i in range(BUFFER_SIZE):
    #   print(shared[i], end=' ')

    # TODO - Display the number of numbers/items received by the reader.
    #        Can not use "items_to_send", must be a value collected
    #        by the reader processes.
    # print(f'{<your variable>} values received')

    smm.shutdown()


if __name__ == '__main__':
    main()
