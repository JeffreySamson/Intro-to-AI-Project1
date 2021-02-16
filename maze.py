
from tkinter import *
from typing import TYPE_CHECKING
import numpy as np
import random
import math
from queue import Empty, PriorityQueue
import heapq
from collections import deque


def main():

    # global variables 
    global SIZE
    global DIM
    global GRID
    global PROB
    global burnRate
    global start
    global end

    #DIM = int(input('Enter the size of the array\n')) # Takes in user input for maze dimesnions
    #PROB = float(input('Enter the probability of an element being a 1 or 0\n')) # Takes in user input for probability of blocked spaces
    #while (PROB <0 or PROB >1):
        #print ('PROB must be between 1 and 0')
        #PROB = float(input('Enter the probability of an element being a 1 or 0\n'))
    burnRate = float(input('Enter the probability of an free space getting burned\n'))
    while (burnRate <0 or burnRate >1):
        print ('PROB must be between 1 and 0')
        burnRate = float(input('Enter the probability of an free space getting burned\n'))
    #DIM = 10
    #PROB = 0.3
    

    searchType = input('How would you like to search for a path? (Enter BFS/DFS or Astar)\n').casefold()
    debug = input('Would you like debugging print statements? (Enter y/n)\n').casefold()
    DIM = 20
    PROB =0.1
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
    checkerBoard()

    # runs search
    if searchType == 'dfs':
        solution = DFS(start, end)
    elif searchType == 'bfs':
        solution = BFS(start,end)
    else:
        solution = AStar(start, end)
    #solution = AStar(start, end)
    print(solution)


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

    #solution2 = BFS(start,end)

    #print("Astar: {} BFS: {}".format(len(solution),len(solution)))



    




######################[functions]######################

def burnGrid(GRID, start, end):
    global burnRate
    global SIZE
    # Make a copy of the maze
    newGrid = np.copy(GRID)
    for node in range(len(GRID)):
        if newGrid[node] != 0 and newGrid[node] != -3 and node != start and node != end:
            neighbors = getBurnedNeighbors(node)
            i = 0
            for j in neighbors:
                if(GRID[j] == -3):
                    i +=1
            prob = 1 - ((1-burnRate)**i)
            if random.uniform(0, 1) <= prob:
                newGrid[node] = -3
    return newGrid

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

        # found the path
        if (v == end):
            print ("Success!")
            return [v] + path
        
        if not processed[v]:

            vldneigh = getNeighbors(v)

            for u in vldneigh:
                if ((d + Heu(u)) < dist[u]):
                    dist[u] = d + Heu(u)
                    #print('going to {} from {} is {}'.format(v,u,dist[u]))
                    heapq.heappush(fringe,(dist[u],u,[u]+path))
                    prev[u] = v
            processed[v] = True

    print("No path")
    return None




# eucledian heuristic
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
            print ("Success!")
            return path + [current]

        # calculate the valid neighbors
        vldneigh = getNeighbors(current)
        #print('Valid Neighbors for {} is {}'.format(current,vldneigh))

        for child in vldneigh:
            if child not in closedSet:
                # new path is path + current for this child
                fringe.append((child,path + [current]))
                closedSet.append(child)

    print("No Solution ")
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

        # pops the top off the stack -> Agent Moves
        current = fringe.pop()
        path.append(current)
        #print("current {}".format(current))

        # found the path
        if (current == end):
            print ("Success!")
            return path
        # calculate the valid neighbors
        GRID = burnGrid(GRID, start, end)
        vldneigh = getNeighbors(current)
        #print('Valid Neighbors for {} is {}'.format(current,vldneigh))

        for child in vldneigh:
            # checks in child is already in the closed set
            if child not in closedSet:
                fringe.append(child)
                #path.append(current)
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
    # Adding spaces already on fire 
    burningSpaces = (SIZE)*burnRate
    burningSpaces = int(round(burningSpaces))

    GRID[start] = -1
    GRID[end] = -2

    c = 0
    while c < numEmpty :
        temp = random.randint(0,SIZE-1)

        if (GRID[temp] == 1 and not(temp ==0) and not(temp == SIZE -1)):
            GRID[temp] = 0
            c +=1

    # Loop to mark the burning spaces 
    c = 0
    while c < burningSpaces:
        temp = random.randint(0,SIZE-1)
        if (GRID[temp] == 1 and not(temp ==0) and not(temp == SIZE -1)):
            GRID[temp] = -3
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
            elif(GRID[i] == -3):
                color = "red" # burning spaces
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
        if not (GRID[i] == 0 or GRID[i] == -3):
            neighbors.append(i)

    return neighbors

def getBurnedNeighbors(current):
    global SIZE
    global GRID
    global DIM

    left = current -1
    right = current+1
    up = current - DIM
    down = current + DIM


    tempNeighbors = [ up, down, right, left] # all possible neighbors
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
    return tempNeighbors

#___________________________________________________________________
# RUN THE MAIN: DO NOT DELETE!
if __name__ == '__main__': main()




