"""
Course: CSE 251
Lesson Week: Week 07
File: team.py
Purpose: Week 05 Team Activity

Instructions:

- Make a copy of your assignment 2 program.  Since you are working in a team,
  you can design which assignment 2 program that you will use for the team
  activity.
- Convert the program to use a process pool and use apply_async() with a
  callback function to retrieve data from the Star Wars website.

"""

from datetime import datetime, timedelta
import requests
import json
import threading

# Include cse 251 common Python files
from cse251 import *
set_working_directory(__file__)

# Const Values
TOP_API_URL = r'https://swapi.dev/api'

# Global Variables
call_count = 0


# TODO Add your threaded class definition here
class request_thread(threading.Thread):
    def __init__(self, url):
        threading.Thread.__init__(self)
        self.url = url
        self.info = {}
        
    def run(self):
        info = requests.get(self.url)
        self.info = info.json()


# TODO Add any functions you need here

def film(url):
    print("GETTING ALL INFO FILM")
    infoFilm = request_thread(url)
    infoFilm.start()
    infoFilm.join()
    infoFilm = infoFilm.info["results"]
    return infoFilm[5]

def data(linkData):
    threads = []
    infoData = []
    for url in linkData:
        infoThread = request_thread(url)
        infoThread.start()
        threads.append(infoThread)
    
    for finish in threads:
        finish.join()
        infoData.append(finish.info["name"])

    return infoData

def palabra(palabras):
    palabra = ''
    for word in palabras:
        palabra += word + ", "

    return palabra


def main():
    log = Log(show_terminal=True)
    log.start_timer('Starting to retrieve data from swapi.dev')

    # TODO Retrieve Top API urls
    starWarsInfo = request_thread(TOP_API_URL)

    starWarsInfo.start()
    starWarsInfo.join()

    def organizing(info):
        infoData = data(infoFilm[info])
        log.write(f'{info.capitalize()}: {len(infoData)}')
        infoData.sort()
        log.write(palabra(infoData))
        log.write('')

    # TODO Retireve Details on film 6

    print("Link for FILMS")
    infoFilm = film(starWarsInfo.info["films"])
    log.write('----------------------------------------')
    log.write(f'Title   : {infoFilm["title"]}')
    log.write(f'Director: {infoFilm["director"]}')
    log.write(f'Producer: {infoFilm["producer"]}')
    log.write(f'Released: {infoFilm["release_date"]}')
    log.write('')


    # TODO Display results
    organizing("characters")
    organizing("planets")
    organizing("starships")
    organizing("vehicles")
    organizing("species")

    log.stop_timer('Total Time To complete')
    log.write(f'There were {call_count} calls to swapi server')
    

if __name__ == "__main__":
    main()
