
from tkinter import *
from typing import TYPE_CHECKING
import numpy as np
import random
from collections import deque

def main():

    # global variables 
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
    end = random.randint(0,SIZE-1)
    #check so that start and end is not the same 
    while (start == end):
        end = random.randint(0,SIZE-1)

    print()
    print("Going from {} -> {}".format(start,end))

    # runing the initial grid
    makeGrid()
    # shows how the initial grid looks like
    #checkerBoard()

    # RUNS DFS 
    solution = DFS(start, end)
    #print(solution)

    # checks if there is a solution and then marks the path
    if solution:
        for i in solution :
            if i > (SIZE -1):
                print("Solution went out of bound at {}".format(i))
            elif not ( i == start or i == end ):
                GRID[i] = 7 # 7 = path

    print() #prints an empty line
    # generates the final solution
    checkerBoard()
    



######################[functions]######################

#executes the BFS algorithm
def BFS(begin,end):

    return


# executes the DFS algorithms
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

    while fringe: # checks if the fringe is empty

        # pops the top off the stack
        current = fringe.pop()
        path.append(current)
        #print("current {}".format(current))

        # found the path
        if (current == end):
            print ("Success!")
            return path
        # calculate the valid neighbors
        vldneigh = getNeighbors(current)
        #print('Valid Neighbors for {} is {}'.format(current,vldneigh))

        for child in vldneigh:
            # checks in child is already in the closed set
            if child not in closedSet:
                fringe.append(child)
            closedSet.append(current)
    print("No Solution ")
    return path
        
    
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
    GRID[end] = -2

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
                color = "white" # not empty
            elif(GRID[i] == 0):
                color = "black" # empty
            elif(GRID[i] == -1):
                color = "blue" # start is blue
            elif(GRID[i] == -2):
                color = "purple" # end is purple
            else:
                color = "green" # path taken
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


    tempNeighbors = [left, right, up, down] # all possible neighbors
    neighbors = [] # valid neighbors

    #checks if the current is on the left edges and gets rid of left neighbor
    if (current % DIM == 0):
        tempNeighbors.remove(left)
    #checks if the current is on the right edges and gets rid of right neighbor
    elif (current % DIM == (DIM -1)):
        tempNeighbors.remove(right)
    #checks if the current is on the down edge and gets rid of down neighbor
    if (current // DIM == (DIM -1)):
        tempNeighbors.remove(down)
    #checks if the current is on the top edge and gets rid of top neighbor
    elif(current //DIM == 0):
        tempNeighbors.remove(up)
    # gets rid of all the nieghbors that are empty
    for i in tempNeighbors:
        if (not GRID[i] == 0):
            neighbors.append(i)

    return neighbors

#___________________________________________________________________
# RUN THE MAIN: DO NOT DELETE!
if __name__ == '__main__': main()




