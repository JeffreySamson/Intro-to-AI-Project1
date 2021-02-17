from tkinter import *
from typing import TYPE_CHECKING
import numpy as np
import random
import math
from queue import Empty, PriorityQueue
import heapq
from collections import deque

# 0: blocked
# -1: start
# -2: end
# 7: path
# -3: fire

def main():

    # global variables 
    global SIZE
    global DIM
    global GRID
    global PROB
    global start
    global end
    global q

    #DIM = int(input('Enter the size of the array: '))
    #PROB = float(input('Enter the probability of an element being a 1 or 0: '))
    #while (PROB <0 or PROB >1):
        #print ('PROB must be between 1 and 0')
        #PROB = float(input('Enter the probability of an element being a 1 or 0: '))

    DIM = 20
    PROB = 0.2
    q = 0.5

    SIZE = DIM**2

    # generates random points to start
    #start = random.randint(0,SIZE-1)
    #end = random.randint(0,SIZE-1)
    start = 0
    end = SIZE - 1


    #check so that start and end is not the same 
    while (start == end):
        end = random.randint(0,SIZE-1)

    print()
    print("Going from {} -> {}".format(start,end))

    # runing the initial grid
    makeGrid()
    # shows how the initial grid looks like


    # runs search
    #solution = AStar(start, end)
    #print(solution)

    #print(solution)

    
    fireSeed = random.randint(0,SIZE-1)

    while (GRID[fireSeed] == 0 or fireSeed == SIZE-1):
        fireSeed = random.randint(0,SIZE-1)

    #print(f"FireSeed is {fireSeed}")
    GRID[fireSeed] = -3


    #solution = AStar(start,end)

    # checks if there is a solution and then marks the path
    
    #if solution:
    #    for i in solution :
    #        if i > (SIZE -1):
    #            print("Solution went out of bound at {}".format(i))
    #        elif not ( i == start or i == end ):
    #           GRID[i] = 7 # 7 = path

    print() #prints an empty line
    # generates the final solution

    #showMaze()
    strategy1()

    #showMaze()
    print()

    



######################[functions]######################

def strategy2():

    return

# executes strategy1
def strategy1():

    path = AStar(start,end)
    
    if not path:
        print("No solution")
        return

    pathLength = len(path)
    #print(path)

    for current in range(pathLength):

        if path[current] == end:
            print("Made it!")
            return

        #moves the guy forward
        GRID[path[current]] = 7

        # moves fire forward
        advFireOneStep()

        # kills guy if he is currently on fire (== -3) or if his next move is on fire
        if (GRID[path[current]] == -3) or ( not (current == pathLength-1) and (GRID[path[current+1]] == -3)):
            showTempMaze()
            print("YOU'RE DEAD!")
            return
        
        # shows the maze
        showTempMaze()

#advances the fire by one step
def advFireOneStep():

    global q
    global GRID

    mazeCopy = np.copy(GRID)

    for current in range(SIZE):

        if not ((mazeCopy[current] == -3) or (mazeCopy[current] ==0)):
            neighbors = getFireNeighbors(current, mazeCopy)
            k = len(neighbors)
            prob = 1-((1-q)**k)
            if random.random() <= prob :
                #print(current)
                GRID[current] = -3
        

    return 

#executes the AStar search algo
def AStar(start,end):
    
    dist = {}
    processed = {}
    prev = {}

    for v in range(SIZE):
        dist[v] = math.inf
        processed[v] = False
        prev[v] = NONE

    dist[start] =0
    fringe = []
    heapq.heappush(fringe,(dist[start],start,[]))
    prev[start] = start
    
    while fringe: # checks if the fringe is empty
        
        (d,v,path) = heapq.heappop(fringe)
        #print(fringe)

        # found the path
        if (v == end):
            #print ("Success!")
            return path
        
        if not processed[v]:

            vldneigh = getNeighbors(v)

            for u in vldneigh:
                if ((d + Heu(u)) < dist[u]):
                    dist[u] = d + Heu(u)
                    #print('going to {} from {} is {}'.format(v,u,dist[u]))
                    heapq.heappush(fringe,(dist[u],u,path + [u]))
                    prev[u] = v
            processed[v] = True

    #print("No path")
    return None

# eucledian heuristic for AStar
def Heu(current):
    global DIM
    global end

    # heuristic is based on eucledian heuristic
    x = current % DIM
    y = current // DIM

    # goal location
    endX = end % DIM
    endY = end // DIM

    # distance formula on (x,y) -> (endX, endY)
    dis = math.sqrt(((x-endX)**2) + (y-endY)**2)

    return dis

#executes the BFS algorithm
def BFS(start,end):
    global GRID

    # checks if the start and the goal is not empty 
    if (GRID[start] == 0 or GRID[end] == 0):
        print("Invalid start or end")
        return

    # creats the stack that you have already visited
    closedSet = []

    # creates the fringe stack and adds start to fringe
    fringe = deque([(start,[])])

    while fringe: # checks if the fringe is empty
        
        # current is the current node
        # path keeps track of the path taken to reach current from start
        #everything at the top of the queue will always be the shortest path
        current, path = fringe.popleft()
        closedSet.append(current)

        # found the path
        if (current == end):
            #print ("Success!")
            path.remove(0)
            return path + [current]

        # calculate the valid neighbors
        vldneigh = getNeighbors(current)
        #print('Valid Neighbors for {} is {}'.format(current,vldneigh))

        for child in vldneigh:
            if child not in closedSet:
                # new path is path + current for this child
                fringe.append((child,path + [current]))
                closedSet.append(child)

    #print("No Solution ")
    return None

# executes the DFS algorithms
def DFS(start, end):
    global GRID
    # checks if the start and the goal is not empty 
    if (GRID[start] == 0 or GRID[end] == 0):
        print("Invalid start or end")
        return

    # creates the fringe stack
    fringe = deque() 
    # adds the start node to the fringe
    fringe.append(start)

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
            #print ("Success!")
            return path
        # calculate the valid neighbors
        vldneigh = getNeighbors(current)
        #print('Valid Neighbors for {} is {}'.format(current,vldneigh))

        for child in vldneigh:
            # checks in child is already in the closed set
            if child not in closedSet:
                fringe.append(child)
                #path.append(current)
        closedSet.append(current)
    #print("No Solution ")
    return None
    
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
class showMaze():
    def __init__(self):
        global DIM
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
            elif(GRID[i] == -3):
                color = "orangered" # on fire
            else:
                color = "green" # path taken
            Canvas(window, width=30, height = 30, bg = color).grid(row = i // DIM, column = i % DIM)

        width = 30*DIM*1.20
        height = 30*DIM*1.20
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()

        # calculate position x and y coordinates
        x = (screen_width/2) - (width/2)
        y = (screen_height/2) - (height/2)
        window.geometry('%dx%d+%d+%d' % (width, height, x, y))
        window.mainloop()

# psuedo animating the maze move
class showTempMaze():

    def __init__(self):
        global DIM
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
            elif(GRID[i] == -3):
                color = "orangered" # on fire
            else:
                color = "green" # path taken
            Canvas(window, width=30, height = 30, bg = color).grid(row = i // DIM, column = i % DIM)

        width = 30*DIM*1.20
        height = 30*DIM*1.20
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()

        # calculate position x and y coordinates
        x = (screen_width/2) - (width/2)
        y = (screen_height/2) - (height/2)
        window.geometry('%dx%d+%d+%d' % (width, height, x, y))
        window.after(450,window.destroy)
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


    tempNeighbors = [ up, down, right, left] # all possible neighbors
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
        if not ((GRID[i] == 0) or (GRID[i] == -3)):
            neighbors.append(i)

    return neighbors

#gets the Neighbors that are on fire
def getFireNeighbors(current, mazeCopy):
    
    global SIZE
    global GRID
    global DIM

    left = current -1
    right = current+1
    up = current - DIM
    down = current + DIM


    tempNeighbors = [ up, down, right, left] # all possible neighbors
    FireNeighbors = [] # valid neighbors

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
        if (mazeCopy[i] ==-3):
            FireNeighbors.append(i)

    return FireNeighbors


#___________________________________________________________________
# RUN THE MAIN: DO NOT DELETE!
if __name__ == '__main__': main()
