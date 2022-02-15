"""
Course: CSE 251
Lesson Week: 06
File: assignment.py
Author: <Your name here>
Purpose: Processing Plant
Instructions:
- Implement the classes to allow gifts to be created.
"""

from datetime import datetime
import random
import multiprocessing as mp
from multiprocessing import Value, Process
import os.path
import time
from turtle import color

# Include cse 251 common Python files - Don't change
from cse251 import *
set_working_directory(__file__)

CONTROL_FILENAME = 'settings.txt'
BOXES_FILENAME   = 'boxes.txt'

# Settings consts
MARBLE_COUNT = 'marble-count'
CREATOR_DELAY = 'creator-delay'
BAG_COUNT = 'bag-count'
BAGGER_DELAY = 'bagger-delay'
ASSEMBLER_DELAY = 'assembler-delay'
WRAPPER_DELAY = 'wrapper-delay'

# No Global variables

class Bag():
    """ bag of marbles - Don't change for the 93% """

    def __init__(self):
        self.items = []

    def add(self, marble):
        self.items.append(marble)

    def get_size(self):
        return len(self.items)

    def __str__(self):
        return str(self.items)


class Gift():
    """ Gift of a large marble and a bag of marbles - Don't change for the 93% """

    def __init__(self, large_marble, marbles):
        self.large_marble = large_marble
        self.marbles = marbles

    def __str__(self):
        marbles = str(self.marbles)
        marbles = marbles.replace("'", "")
        return f'Large marble: {self.large_marble}, marbles: {marbles[1:-1]}'


class Marble_Creator(mp.Process):
    """ This class "creates" marbles and sends them to the bagger """


    def __init__(self, limit, sendMarbles, delay):
        # TODO Add any arguments and variables here
        mp.Process.__init__(self)
        self.limit = limit
        self.sendMarbles = sendMarbles
        self.delay = delay
        self.colors = ('Gold', 'Orange Peel', 'Purple Plum', 'Blue', 'Neon Silver', 
        'Tuscan Brown', 'La Salle Green', 'Spanish Orange', 'Pale Goldenrod', 'Orange Soda', 
        'Maximum Purple', 'Neon Pink', 'Light Orchid', 'Russian Violet', 'Sheen Green', 
        'Isabelline', 'Ruby', 'Emerald', 'Middle Red Purple', 'Royal Orange', 'Big Dip O’ruby', 
        'Dark Fuchsia', 'Slate Blue', 'Neon Dark Green', 'Sage', 'Pale Taupe', 'Silver Pink', 
        'Stop Red', 'Eerie Black', 'Indigo', 'Ivory', 'Granny Smith Apple', 
        'Maximum Blue', 'Pale Cerulean', 'Vegas Gold', 'Mulberry', 'Mango Tango', 
        'Fiery Rose', 'Mode Beige', 'Platinum', 'Lilac Luster', 'Duke Blue', 'Candy Pink', 
        'Maximum Violet', 'Spanish Carmine', 'Antique Brass', 'Pale Plum', 'Dark Moss Green', 
        'Mint Cream', 'Shandy', 'Cotton Candy', 'Beaver', 'Rose Quartz', 'Purple', 
        'Almond', 'Zomp', 'Middle Green Yellow', 'Auburn', 'Chinese Red', 'Cobalt Blue', 
        'Lumber', 'Honeydew', 'Icterine', 'Golden Yellow', 'Silver Chalice', 'Lavender Blue', 
        'Outrageous Orange', 'Spanish Pink', 'Liver Chestnut', 'Mimi Pink', 'Royal Red', 'Arylide Yellow', 
        'Rose Dust', 'Terra Cotta', 'Lemon Lime', 'Bistre Brown', 'Venetian Red', 'Brink Pink', 
        'Russian Green', 'Blue Bell', 'Green', 'Black Coral', 'Thulian Pink', 
        'Safety Yellow', 'White Smoke', 'Pastel Gray', 'Orange Soda', 'Lavender Purple',
        'Brown', 'Gold', 'Blue-Green', 'Antique Bronze', 'Mint Green', 'Royal Blue', 
        'Light Orange', 'Pastel Blue', 'Middle Green')

    def run(self):
        '''
        for each marble:
            send the marble (one at a time) to the bagger
              - A marble is a random name from the colors list above
            sleep the required amount
        Let the bagger know there are no more marbles
        '''
        
        for i in range(self.limit):
            self.sendMarbles.send(random.choice(self.colors))
            time.sleep(self.delay)

            

        self.sendMarbles.close()
        pass


class Bagger(mp.Process):
    """ Receives marbles from the marble creator, then there are enough
        marbles, the bag of marbles are sent to the assembler """
    def __init__(self, marblesQuantity, receiveMarbles, bagQuantity, sendBags, delay, giftCount):
        mp.Process.__init__(self)
        # TODO Add any arguments and variables here
        self.marblesQuan = marblesQuantity
        self.receiveMarbles = receiveMarbles
        self.bagQuantity = bagQuantity
        self.sendBags = sendBags
        self.delay = delay
        self.giftCount = giftCount

    def run(self):
        '''
        while there are marbles to process
            collect enough marbles for a bag
            send the bag to the assembler
            sleep the required amount
        tell the assembler that there are no more bags
        '''
        newBag = Bag()

        for i in range(self.marblesQuan):
            newBag.add(self.receiveMarbles.recv())
            if (((newBag.get_size() % self.bagQuantity) == 0)):
                # print(f'Sending Bag: {newBag.items}')
                self.sendBags.send(newBag)
                self.giftCount.value += 1
                time.sleep(self.delay)
                newBag.items = []
            
        
        self.sendBags.send('STOP')
        self.sendBags.close()


class Assembler(mp.Process):
    """ Take the set of marbles and create a gift from them.
        Sends the completed gift to the wrapper """

    def __init__(self, quantityBags, receiveBags, delay, sendGifts):
        mp.Process.__init__(self)
        # TODO Add any arguments and variables here
        self.quantityBags = quantityBags
        self.receivebags = receiveBags
        self.delay = delay
        self.sendGifts = sendGifts
        self.marble_names = ('Lucky', 'Spinner', 'Sure Shot', 'The Boss', 'Winner', '5-Star', 'Hercules', 'Apollo', 'Zeus')

    def run(self):
        '''
        while there are bags to process
            create a gift with a large marble (random from the name list) and the bag of marbles
            send the gift to the wrapper
            sleep the required amount
        tell the wrapper that there are no more gifts
        '''
        while True:
            randomLargoMarble = random.choice(self.marble_names)
            x = self.receivebags.recv()
            newGift = Gift(randomLargoMarble, x)
            self.sendGifts.send(newGift)
           
            if(x == 'STOP'):
                self.sendGifts.send('STOP')
                self.sendGifts.close()
                break
        
            time.sleep(self.delay)





class Wrapper(mp.Process):
    """ Takes created gifts and wraps them by placing them in the boxes file """
    def __init__(self, receiveGifts, delay):
        mp.Process.__init__(self)
        # TODO Add any arguments and variables here
        self.receiveGifts = receiveGifts
        self.delay = delay


    def run(self):
        '''
        open file for writing
        while there are gifts to process
            save gift to the file with the current time
            sleep the required amount
        '''
        fileBox = open('boxes.txt', 'w')

        while True:
            x = self.receiveGifts.recv()

            if(x == 'STOP'):
                break
            else:
                fileBox.write(f'Created - {datetime.now().time()}:{x}\n')

            time.sleep(self.delay)
        
        fileBox.close()



def display_final_boxes(filename, log):
    """ Display the final boxes file to the log file -  Don't change """
    if os.path.exists(filename):
        log.write(f'Contents of {filename}')
        with open(filename) as boxes_file:
            for line in boxes_file:
                log.write(line.strip())
    else:
        log.write_error(f'The file {filename} doesn\'t exist.  No boxes were created.')



def main():
    """ Main function """

    log = Log(show_terminal=True)

    log.start_timer()

    # Load settings file
    settings = load_json_file(CONTROL_FILENAME)
    if settings == {}:
        log.write_error(f'Problem reading in settings file: {CONTROL_FILENAME}')
        return

    log.write(f'Marble count                = {settings[MARBLE_COUNT]}')
    log.write(f'settings["creator-delay"]   = {settings[CREATOR_DELAY]}')
    log.write(f'settings["bag-count"]       = {settings[BAG_COUNT]}') 
    log.write(f'settings["bagger-delay"]    = {settings[BAGGER_DELAY]}')
    log.write(f'settings["assembler-delay"] = {settings[ASSEMBLER_DELAY]}')
    log.write(f'settings["wrapper-delay"]   = {settings[WRAPPER_DELAY]}')

    # TODO: create Pipes between creator -> bagger -> assembler -> wrapper

    sendMarbles_conn1, receiveMarbles_conn1 = mp.Pipe()
    sendBags_conn2, receiveBags_conn2 = mp.Pipe()
    sendGifts_conn3, receiveGifts_conn3= mp.Pipe()

    # TODO create variable to be used to count the number of gifts

    giftCount = Value('i', 0)

    # delete final boxes file
    if os.path.exists(BOXES_FILENAME):
        os.remove(BOXES_FILENAME)

    log.write('Create the processes')

    # TODO Create the processes (ie., classes above)

    createMarble = Marble_Creator(settings[MARBLE_COUNT], sendMarbles_conn1, settings[CREATOR_DELAY])
    createBagger = Bagger(settings[MARBLE_COUNT], receiveMarbles_conn1,settings[BAG_COUNT], sendBags_conn2, settings[BAGGER_DELAY], giftCount)
    createAssembler = Assembler(giftCount, receiveBags_conn2, settings[ASSEMBLER_DELAY], sendGifts_conn3)
    createWrapper = Wrapper(receiveGifts_conn3, settings[WRAPPER_DELAY])

    log.write('Starting the processes')
    # TODO add code here
    createMarble.start()
    createBagger.start()
    createAssembler.start()
    createWrapper.start()

    log.write('Waiting for processes to finish')
    # TODO add code here
    createMarble.join()
    createBagger.join()
    createAssembler.join()
    createWrapper.join()


    display_final_boxes(BOXES_FILENAME, log)
    # TODO Log the number of gifts created.



if __name__ == '__main__':
    main()

