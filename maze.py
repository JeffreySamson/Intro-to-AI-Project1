
from tkinter import *
from typing import TYPE_CHECKING
import numpy as np
import random
from collections import deque

def main():

    global SIZE
    global DIM
    global GRID
    global PROB
    global start
    global end

    #DIM = int(input('Enter the size of the array: '))
    #PROB = float(input('Enter the probability of an element being a 1 or 0: '))
    #while (PROB <0 or PROB >1):
        #print ('PROB must be between 1 and 0')
        #PROB = float(input('Enter the probability of an element being a 1 or 0: '))

    DIM = 10
    PROB = 0.3
    SIZE = DIM**2

    # generates random points to start
    start = random.randint(0,SIZE-1)
    print('Starting from: {}'.format(start))
    end = random.randint(0,SIZE-1)
    print('Ending at: {}'.format(end))

    print()
    print("Going from {} -> {}".format(start,end))

    # runing Visuals
    makeGrid()
    checkerBoard()


    # RUNS DFS 
    solution = BFS(start, end)
    print(solution)

    # checks if there is a solution and then marks the path
    if solution:
        for i in solution :
            if i > (SIZE -1):
                print("Solution went out of bound at {}".format(i))
            elif not ( i == start or i == end ):
                GRID[i] = 7 # draws the path in a different color

    # generates the final solution
    checkerBoard()


######################[functions]######################

def DFS(begin, end):
    global GRID
    # checks if the start and the goal is not empty 
    if (GRID[begin] == 0 or GRID[end] == 0):
        print("Invalid start or end")
        return

    # creates the fringe stack
    fringe = deque() 
    # adds the start node to the fringe
    fringe.append(begin)

    # creats the stack that you have already visited
    closedSet = deque() #

    # path to the solution
    path = []
    i = 0
    while fringe: # checks if the fringe is empty
        # pops the top off the stack
        print('STEP {}'.format(i))
        current = fringe.pop()
        print('Current is {}'.format(current))
        path.append(current)
        print("Path is {}".format(path))

        # found the path
        if (current == end):
            print ("Success!")
            return path
        # calculate the valid neighbors
        vldneigh = getNeighbors(current)
        print('Valid Neighbors for {} is {}'.format(current,vldneigh))

        for child in vldneigh:
            # checks in child is already in the closed set
            if child not in closedSet:
                fringe.append(child)
            closedSet.append(current)
        print('closed set is {}'.format(closedSet))
        i += 1

    print("No Solution ")

def BFS(begin, end):
    global GRID
    # checks if the start and the goal is not empty 
    if (GRID[begin] == 0 or GRID[end] == 0):
        print("Invalid start or end")
        return

    # creates the fringe stack
    fringe = deque() 
    # adds the start node to the fringe
    fringe.append(begin)

    # creats the stack that you have already visited
    closedSet = deque() #

    # path to the solution
    path = []
    i = 0
    while fringe: # checks if the fringe is empty
        # pops the top off the stack
        print('fringe is: {}'.format(fringe))
        print('\n')
        print('STEP {}'.format(i))
        current = fringe.popleft()
        print('Current is {}'.format(current))
        path.append(current)
        print("Path is {}".format(path))

        # found the path
        if (current == end):
            print ("Success!")
            return path
        # calculate the valid neighbors
        vldneigh = getNeighbors(current)
        print('Valid Neighbors for {} is {}'.format(current,vldneigh))

        for child in vldneigh:
            # checks in child is already in the closed set
            if child not in closedSet:
                fringe.append(child)
        closedSet.append(current)
        print('closed set is {}'.format(closedSet))
        i += 1
        

    print("No Solution ")        
    
# makes the grid using the probability and the size
def makeGrid():
    global SIZE
    global DIM
    global GRID
    global start
    global end

    GRID = np.ones(DIM**2)

    numEmpty = (SIZE)*PROB
    numEmpty = int(round(numEmpty))

    GRID[start] = -1
    GRID[end] = -1

    c = 0
    while c < numEmpty :
        temp = random.randint(0,SIZE-1)

        if (GRID[temp] == 1 and not(temp ==0) and not(temp == SIZE -1)):
            GRID[temp] = 0
            c +=1


# makes the visual canvas for the grid
class checkerBoard():
    def __init__(self):
        
        # makes the window for the maze
        window = Tk()
        window.title("Fire Maze")

        # makes the grid all white
        for i in range(SIZE):
            if(GRID[i] == 1):
                color = "white"
            elif(GRID[i] == 0):
                color = "black"
            elif(GRID[i] == -1):
                color = "orange"
            else:
                color = "green"
            Canvas(window, width=30, height = 30, bg = color).grid(row = i // DIM, column = i % DIM)
    
        window.mainloop()

# gets the left, right, up, and down neighbors in that order
def getNeighbors(current):
    global SIZE
    global GRID
    global DIM

    left = current -1
    right = current+1
    up = current - DIM
    down = current + DIM


    temp = [left, down, right, up]
    neighbors = []

    #checks if the current is on the edges and gets rid of apporopriate neighbor
        # Case for current is in the left most column with neighbor in the right most column one above
    if (current % DIM == 0): 
        temp.remove(left)
        # Case for current is in the right most column with neighbor in the left most column one below
    elif (current % DIM == (DIM -1)):
        temp.remove(right)
        # Case for current is in the bottom most row
    if (current // DIM == (DIM -1)):
        temp.remove(down)
        # Case for current is in the top most row
    elif(current //DIM == 0):
        temp.remove(up)

    for i in temp:
        if (not GRID[i] == 0):
            neighbors.append(i)

    return neighbors


# RUN THE MAIN: DO NOT DELETE!
if __name__ == '__main__': main()




