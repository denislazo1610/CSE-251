"""
Course: CSE 251
Lesson Week: 02 - Team Activity
File: team.py
Author: Brother Comeau

Purpose: Playing Card API calls

Instructions:

- Review instructions in I-Learn.

"""

from datetime import datetime, timedelta
import threading
import requests
import json

# Include cse 251 common Python files
from cse251 import *
set_working_directory(__file__)

# TODO Create a class based on (threading.Thread) that will
# make the API call to request data from the website

class Request_thread(threading.Thread):
    # TODO - Add code to make an API call and return the results

    def __init__(self, url):
        # calling parent class constructor
        threading.Thread.__init__(self)
        self.url = url
        self.reponse = {}


    def run(self):
        info = requests.get(self.url)
        self.response = info.json()
        # print_dict(self.response)
    
        
    	

    # https://realpython.com/python-requests/
    pass

class Deck:

    def __init__(self, deck_id):
        self.id = deck_id
        self.reshuffle()
        self.remaining = 52


    def reshuffle(self):
        # TODO - add call to reshuffle
        print("Reshuffle starts")
        reshuffle = Request_thread(f'http://deckofcardsapi.com/api/deck/{self.id}/shuffle/')
        reshuffle.start()
        reshuffle.join()
        print("Reshuffle ends")
        
        # print_dict(reshuffleInfo)
        pass

    def draw_card(self):
        # print("Draw starts")
        draw = Request_thread(f'http://deckofcardsapi.com/api/deck/{self.id}/draw/')
        draw.start()
        draw.join()
        # if draw.response["cards"] != []:
            
        return draw.response["cards"][0]['code']

        # print("Draw ends")
        # TODO add call to get a card
        pass

    def cards_remaining(self):
        return self.remaining


    def draw_endless(self):
        if self.remaining <= 0:
            self.reshuffle()
        return self.draw_card()


if __name__ == '__main__':

    # TODO - run the program team_get_deck_id.py and insert
    #        the deck ID here.  You only need to run the 
    #        team_get_deck_id.py program once. You can have
    #        multiple decks if you need them

    deck_id = 'krsljgciu1w2'

    # Testing Code >>>>>
    deck = Deck(deck_id)
    for i in range(55):
        card = deck.draw_endless()
        print(i, card, flush=True)
    print()
    # <<<<<<<<<<<<<<<<<<

