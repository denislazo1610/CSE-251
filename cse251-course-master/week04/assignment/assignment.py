"""
Course: CSE 251
Lesson Week: 04
File: assignment.py
Author: <Your name>

Purpose: Assignment 04 - Factory and Dealership

Instructions:

- See I-Learn

"""

from asyncio import Queue
from multiprocessing import Semaphore
import queue
import time
import threading
import random

# Include cse 251 common Python files
from cse251 import *
set_working_directory(__file__)

# Global Consts - Do not change
CARS_TO_PRODUCE = 500 # 500
MAX_QUEUE_SIZE = 10 #10
SLEEP_REDUCE_FACTOR = 50 #50

# NO GLOBAL VARIABLES!

class Car():
    """ This is the Car class that will be created by the factories """

    # Class Variables
    car_makes = ('Ford', 'Chevrolet', 'Dodge', 'Fiat', 'Volvo', 'Infiniti', 'Jeep', 'Subaru', 
                'Buick', 'Volkswagen', 'Chrysler', 'Smart', 'Nissan', 'Toyota', 'Lexus', 
                'Mitsubishi', 'Mazda', 'Hyundai', 'Kia', 'Acura', 'Honda')

    car_models = ('A1', 'M1', 'XOX', 'XL', 'XLS', 'XLE' ,'Super' ,'Tall' ,'Flat', 'Middle', 'Round',
                'A2', 'M1X', 'SE', 'SXE', 'MM', 'Charger', 'Grand', 'Viper', 'F150', 'Town', 'Ranger',
                'G35', 'Titan', 'M5', 'GX', 'Sport', 'RX')

    car_years = [i for i in range(1990, datetime.now().year)]

    def __init__(self):
        # Make a random car
        self.model = random.choice(Car.car_models)
        self.make = random.choice(Car.car_makes)
        self.year = random.choice(Car.car_years)

        # Sleep a little.  Last statement in this for loop - don't change
        time.sleep(random.random() / (SLEEP_REDUCE_FACTOR))

        # Display the car that has just be created in the terminal
        self.display()
           
    def display(self):
        print(f'{self.make} {self.model}, {self.year}')


class Queue251():
    """ This is the queue object to use for this assignment. Do not modify!! """

    def __init__(self):
        self.items = []

    def size(self):
        return len(self.items)

    def put(self, item):
        self.items.append(item)

    def get(self):
        return self.items.pop(0)


class Factory(threading.Thread):
    """ This is a factory.  It will create cars and place them on the car queue """

    def __init__(self, queue, empty, full):
        # TODO, you need to add arguments that will pass all of data that 1 factory needs
        # to create cars and to place them in a queue.
        threading.Thread.__init__(self)
        self.newCars= queue 
        self.empty = empty
        self.full = full
        self.number = 0




    def run(self):
        for i in range(CARS_TO_PRODUCE):
            # TODO Add you code here
            """
            create a car
            place the car on the queue
            signal the dealer that there is a car on the queue
           """

            self.full.acquire()
            
            newCar = Car()
            self.newCars.put(newCar)
            self.number += 1
            print(f'We made N{self.number} car')
            self.empty.release()

            print(' -FACTORY')
            print('\n')
        # signal the dealer that there there are not more cars
        pass


class Dealer(threading.Thread):
    """ This is a dealer that receives cars """

    def __init__(self, queue, goal, stats, empty, full):
        # TODO, you need to add arguments that pass all of data that 1 Dealer needs
        # to sell a car
        threading.Thread.__init__(self)
        self.cars = queue
        self.goal = goal # CARS_TO_PRODUCE
        self.stats = stats
        self.empty = empty
        self.full = full
        self.quantitySold = 0
        pass

    def run(self):
        while True:
            # TODO Add your code here
            """
            take the car from the queue
            signal the factory that there is an empty slot in the queue
            """

            if(self.quantitySold == self.goal):
                break

            self.empty.acquire()


            self.stats[self.cars.size()] += 1

                
            outCar = self.cars.get()

            self.quantitySold = self.quantitySold + 1
            print(f'We sold {self.quantitySold} cars')

            

            time.sleep(random.random() / (SLEEP_REDUCE_FACTOR))
            self.full.release()



            print("-Dealer")
            print('\n')




            # Last statement in this for loop - don't change
            pass



def main():
    log = Log(show_terminal=True)

    # TODO Create semaphore(s)
    full = Semaphore(10)
    
    empty = Semaphore(0)
    
    # TODO Create queue251 
    newQueue = Queue251()

    # TODO Create lock(s) ?

    # This tracks the length of the car queue during receiving cars by the dealership
    # i.e., update this list each time the dealer receives a car
    queue_stats = [0] * MAX_QUEUE_SIZE

    # TODO create your one factory

    newFactory = Factory(newQueue, empty, full)


    # TODO create your one dealership

    newDealerShip = Dealer(newQueue, CARS_TO_PRODUCE, queue_stats, empty, full)

    log.start_timer()

    # TODO Start factory and dealership


    newFactory.start()
    newDealerShip.start()

    newDealerShip.join()
    newFactory.join()


    print("\nThings in QUEUE") 

    for i in newQueue.items:
        i.display()

    print(f'Queau has {newQueue.size()} cars')

    # TODO Wait for factory and dealership to complete

    log.stop_timer(f'All {sum(queue_stats)} have been created')

    xaxis = [i for i in range(1, MAX_QUEUE_SIZE + 1)]
    plot = Plots()
    plot.bar(xaxis, queue_stats, title=f'{sum(queue_stats)} Produced: Count VS Queue Size', x_label='Queue Size', y_label='Count')



if __name__ == '__main__':
    main()
