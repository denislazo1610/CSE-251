"""
Course: CSE 251 
Lesson Week: 09
File: assignment09-p1.py 
Author: <Add name here>

Purpose: Part 1 of assignment 09, finding a path to the end position in a maze

Instructions:
- Do not create classes for this assignment, just functions
- Do not use any other Python modules other than the ones included

"""
# from curses import COLOR_BLACK
import math
from screen import Screen
from maze import Maze, COLOR_BLACK, COLOR_VISITED
import cv2, sys

# Include cse 251 common Python files - Dont change
from cse251 import *
set_working_directory(__file__)

SCREEN_SIZE = 800
COLOR = (0, 0, 255)


# TODO add any functions
def recursionPath(path, maze):
    lastSpot = path[-1]
    maze.move(*lastSpot, COLOR)
    possibleMoves = maze.get_possible_moves(*lastSpot)


    if(maze.at_end(*lastSpot) != True):
        if(len(possibleMoves) == 1):
            
            path.append(*possibleMoves)
            info = recursionPath(path, maze)
            if (info == 'Dead End'):
                spotRemove = path.pop()
                maze.restore(*spotRemove)
                return 'Dead End'
            else:
                return info


        elif(len(possibleMoves) == 0):
            
            spotRemove = path.pop()
            maze.restore(*spotRemove)
            return 'Dead End'


        else:
            
            for i in possibleMoves:
                path.append(i)
                info = recursionPath(path, maze)
                if (info != 'Dead End'):
                    lastspot = info[-1]
                    if (maze.at_end(*lastspot)):
                        return info
                
            spotRemove = path.pop()
            maze.restore(*spotRemove)
            return 'Dead End'


    return path

def solve_path(maze):
    """ Solve the maze and return the path found between the start and end positions.  
        The path is a list of positions, (x, y) """
        
    # TODO start add code here
    path = []
    start = maze.get_start_pos()
    path.append(start) 

    path = recursionPath(path, maze)

    return path


def get_path(log, filename):
    """ Do not change this function """

    # create a Screen Object that will contain all of the drawing commands
    screen = Screen(SCREEN_SIZE, SCREEN_SIZE)
    screen.background((255, 255, 0))

    maze = Maze(screen, SCREEN_SIZE, SCREEN_SIZE, filename)

    path = solve_path(maze)

    log.write(f'Number of drawing commands for = {screen.get_command_count()}')

    done = False
    speed = 1
    while not done:
        if screen.play_commands(speed): 
            key = cv2.waitKey(0)
            if key == ord('+'):
                speed = max(0, speed - 1)
            elif key == ord('-'):
                speed += 1
            elif key != ord('p'):
                done = True
        else:
            done = True

    return path


def find_paths(log):
    """ Do not change this function """

    files = ('verysmall.bmp', 'verysmall-loops.bmp', 
            'small.bmp', 'small-loops.bmp', 
            'small-odd.bmp', 'small-open.bmp', 'large.bmp', 'large-loops.bmp')

    # files = ('verysmall.bmp', 'verysmall-loops.bmp',)

    

    log.write('*' * 40)
    log.write('Part 1')
    for filename in files:
        log.write()
        log.write(f'File: {filename}')
        path = get_path(log, filename)
        log.write(f'Found path has length          = {len(path)}')
    log.write('*' * 40)


def main():
    """ Do not change this function """
    sys.setrecursionlimit(5000)
    log = Log(show_terminal=True)
    find_paths(log)


if __name__ == "__main__":
    main()