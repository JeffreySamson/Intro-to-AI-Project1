
from tkinter import *
import numpy as np
import random
from collections import deque

def main():

    global SIZE
    global DIM
    global PROB
    global GRID

    #DIM = int(input('Enter the size of the array: '))
    #PROB = float(input('Enter the probability of an element being a 1 or 0: '))
    #while (PROB <0 or PROB >1):
        #print ('PROB must be between 1 and 0')
        #PROB = float(input('Enter the probability of an element being a 1 or 0: '))

    DIM = 10
    PROB = 0.6

    SIZE = DIM**2
    GRID = np.ones(DIM**2)

    # runing Visuals
    makeGrid()
    checkerBoard()

    #start = random.randint(0,SIZE-1)
    #end = random.randint(0,SIZE-1)

    solution = DFS(0,17)
    print (solution)

    for i in solution :
        GRID[i] = -1


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

    while fringe: # checks if the fringe is empty

        # pops the top off the stack
        current = fringe.pop()
        path.append(current)
        print("current {}".format(current))

        # found the path
        if (current == end):
            print ("Success!")
            return path
        # calculate the valid neighbors
        vldneigh = getNeighbors(current)
        print('Valid Neighbors for current: {}'.format(vldneigh))

        for child in vldneigh:
            # checks in child is already in the closed set
            if child not in closedSet:
                fringe.append(child)
            closedSet.append(current)
            
    
    print("No Solution")
        
    
# makes the grid using the probability and the size
def makeGrid():
    global SIZE
    global DIM
    numEmpty = (SIZE)*PROB
    numEmpty = int(round(numEmpty))

    c = 0
    while c < numEmpty :
        temp = random.randint(0,SIZE-1)

        if (GRID[temp] == 1):
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
            elif(GRID[i] == -10):
                color = "orange"
            else:
                color = "green"
            Canvas(window, width=30, height = 30, bg = color).grid(row = i // DIM, column = i % DIM)
    
        window.mainloop()

# gets the left, right, up, and down neighbors in that order
def getNeighbors(current):
    left = current -1
    right = current+1
    up = current - DIM
    down = current + DIM
    neigh = [left, right, up, down]

    #checks if the current is on the edges and gets rid of apporopriate neighbor
    if (current % DIM == 0):
        neigh.remove(left)
    elif (current % DIM == (DIM -1)):
        neigh.remove(right)

    for i in neigh:
        if((i < 0) or (i > (SIZE -1))):
            neigh.remove(i)
        elif(GRID[i] ==0):
            neigh.remove(i)
    return neigh


# RUN THE MAIN: DO NOT DELETE!
if __name__ == '__main__': main()




