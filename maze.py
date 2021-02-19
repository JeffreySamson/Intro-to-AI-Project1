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
# 5: move back
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

    # Recieving User input for our variables 
    DIM = int(input('Enter the size of the array: '))
    while DIM < 0:
        print("DIM cannot be less than 0.\n")
        DIM = int(input('Enter the size of the array: \n'))
    PROB = float(input('Enter the probability of an element being a 1 or 0: \n'))
        # pobablility has to be a decimal value
    while (PROB <0 or PROB >1):
        print ('PROB must be between 1 and 0')
        PROB = float(input('Enter the probability of an element being a 1 or 0: \n'))
    
   

    # INSERT START AND END POINTS
   

    #DIM = 10
    #PROB = 0.2
    #q = 0.2

    SIZE = DIM**2

    startEnd = input('Random or default start and end? \n(Default is upper-left for start and bottom-right for end) \n(Enter random or default): \n').casefold().strip()
    while not ((startEnd == 'random') or (startEnd == 'default')):
        print ('Must enter random or default')
        startEnd = input('Random or default start and end (Default is upper-left for start and bottom-right for end) (Enter random or default): ')
    if (startEnd == 'random'):
        # generates random points to start
        start = random.randint(0,SIZE-1)
        end = random.randint(0,SIZE-1)
    else:
        start = 0
        end = SIZE - 1
    #start = 0
    #end = SIZE - 1

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

    



    #solution = DFS(start,end)

    # checks if there is a solution and then marks the path
    
    #if solution:
    #    for i in solution :
    #        if GRID[i] == 7 :
    #            GRID[i] = 5
    #        elif not ( i == start or i == end ):
    #          GRID[i] = 7 # 7 = path

    print() #prints an empty line
    # generates the final solution

    mazeCopy = np.copy(GRID)

    print()

    #strategy2(start,end)
    exit = False
    while not exit:
        searchOrStrat = (input('Would you like to see a search type or strategy? (search type / strategy) \n')).casefold().strip()
        if searchOrStrat == 'search type':
            print()
            searchType = input('Enter which search type you would like to use (BFS, DFS, Astar): \n').casefold().strip()
            if searchType == "dfs":
                path = DFS(start,end)
                if path:
                    #print(path)
                    paintGRID(path)
                else: 
                    print("No path")
                exit = True
            elif searchType == "bfs":
                path = BFS(start,end)
                if path:
                    paintGRID(path)
                else: 
                    print("No path")
                exit = True
            elif searchType == "astar":
                path = AStar(start,end)
                if path :
                    paintGRID(path)
                else:
                    print("No path!")
                exit = True
            else: print("Not a valid search type.")

        elif searchOrStrat == 'strategy':
            q = float(input('Enter the flammability rate: \n'))
                # pobablility has to be a decimal value
            while (q <0 or q >1):
                print ('Flammability rate must be between 1 and 0')
                q = float(input('Enter the flammability rat: \n'))
            
            
            # randomly starts the fire
            fireSeed = random.randint(0,SIZE-1)

            # fire can't start at the beginning or end
            while (GRID[fireSeed] == 0 or fireSeed == SIZE-1):
                fireSeed = random.randint(0,SIZE-1)

            #print(f"FireSeed is {fireSeed}")
            GRID[fireSeed] = -3

            print()
            strategy = int(input('Enter which strategy you would like to use (1, 2, 3): \n'))
            if strategy == 1:
                strategy1(start,end)
                exit = True
            elif strategy == 2:
                strategy2(start,end)
                exit = True
            elif strategy == 3:
                strategy3(start,end)
                exit = True
            else: print("Not a valid strategy")

        else:
            print("Oops something went wrong. Try again!")

    #GRID = mazeCopy

    #showMaze()
    #strategy3(start,end)


    #showMaze()
    print()


######################[functions]######################

def paintGRID(path):

    global GRID

    showTempMaze()

    for i in path:

        if (i not in getNeighbors(i-1)) :
            
            backtrack = BFS(i-1,i)
            
            for j in backtrack:
                GRID[i]= 5

        else:
            GRID[i] = 7

        showTempMaze()
    return


def strategy3(start,end):


    global GRID

    # initial search to see if there is a solution
    path = AStarMod(start,end)

    if not path:
        print("No Solution")
        return

    current = start

    while not path[0] == end:
        
        # checks the shortest path each time
        path = AStarMod(current,end)


        if (not path):
            print("SORRY NO SAFE PATH!")
            showMaze()
            return



        if GRID[path[0]] == 7:
            GRID[path[0]] = 5
        else:
            GRID[path[0]] = 7


        current = path[0]

        if current == end:
            print("MADE IT!")
            return

        advFireOneStep()

        if (GRID[current] == -3):
            print("YOU'RE ON FIRE!")
            GRID[current] = 6
            showMaze()
            return


        showTempMaze()
    

    print("MADE IT!")
    return

# creates a new heuristic that takes into account the fire and it's neighbors
def heu2(current,end):

    global SIZE

    #euclidean distance
    dis = diagDis(current,end)

    # distance from fire 
    fire = diagDis(current,findFire(current))

    if fire <= 2:
        dis = dis + (SIZE-fire) + len(getFireNeighbors(current,GRID))

    return dis

def findFire(current):
    global GRID

    # creats the stack that you have already visited
    closedSet = []

    # creates the fringe stack and adds start to fringe
    fringe = deque([(current,[])])

    while fringe: # checks if the fringe is empty
        
        # current is the current node
        # path keeps track of the path taken to reach current from start
        #everything at the top of the queue will always be the shortest path
        current, path = fringe.popleft()
        closedSet.append(current)

        # found the path
        if (GRID[current] == -3):
            #print ("Success!")
            return current

        # calculate the valid neighbors
        vldneigh = getNeighbors(current) + getFireNeighbors(current,GRID)

        #print('Valid Neighbors for {} is {}'.format(current,vldneigh))

        for child in vldneigh:
            if child not in closedSet:
                # new path is path + current for this child
                fringe.append((child,path + [current]))
                closedSet.append(child)

    #print("No Solution ")
    return None

def AStarMod(start,end):
    
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
                if ((d + heu2(u,end)) < dist[u]):
                    dist[u] = d + heu2(u,end)
                    #print('going to {} from {} is {}'.format(v,u,dist[u]))
                    heapq.heappush(fringe,(dist[u],u,path + [u]))
                    prev[u] = v
            processed[v] = True

    #print("No path")
    return None

# keeps track of current fire and creates a new path but never expects the future
def strategy2(start,end):

    global GRID

    # change this
    path = AStar(start,end)

    if not path:
        print("No Solution")
        return

    current = start

    while not path[0] == end:
        
        #change this
        path = AStar(current,end)


        if (not path):
            print("SORRY NO SAFE PATH!")
            showMaze()
            return



        if GRID[path[0]] == 7:
            GRID[path[0]] = 5
        else:
            GRID[path[0]] = 7


        current = path[0]

        if current == end:
            print("MADE IT!")
            return

        advFireOneStep()

        if (GRID[current] == -3):
            print("YOU'RE ON FIRE!")
            GRID[current] = 6
            showMaze()
            return


        showTempMaze()
    

    print("MADE IT!")
    return

# executes strategy1
def strategy1(start,end):

    global GRID
    # initial search
    path = AStar(start,end)
    
    if not path:
        print("No solution")
        return

    pathLength = len(path)
    #print(path)

    for current in range(pathLength):

        if (GRID[path[current]] == -3):
            print("YOU'RE ON FIRE!")
            GRID[path[current]] = 6
            showMaze()
            return

        if path[current] == end:
            print("Made it!")
            return

        #moves the guy forward
        if GRID[path[current]] == 7:
            GRID[path[current]] = 5
        else:
            GRID[path[current]] = 7

        # moves fire forward
        advFireOneStep()

        # kills guy if he is currently on fire (== -3) or if his next move is on fire
        if (GRID[path[current]] == -3): #or ( not (current == pathLength-1) and (GRID[path[current+1]] == -3)):
            print("YOU'RE ON FIRE!")
            GRID[path[current]] = 6
            showMaze()
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
                if ((d + diagDis(u,end)) < dist[u]):
                    dist[u] = d + diagDis(u,end)
                    #print('going to {} from {} is {}'.format(v,u,dist[u]))
                    heapq.heappush(fringe,(dist[u],u,path + [u]))
                    prev[u] = v
            processed[v] = True

    #print("No path")
    return None

# eucledian heuristic for AStar
def diagDis(current,end):
    global DIM

    # heuristic is based on eucledian heuristic
    x = current % DIM
    y = current // DIM

    #print(x,y)


    # goal location
    endX = (end % DIM)
    endY = end // DIM

    #print(endX,endY)

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
            path.remove(start)
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
        return None

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
            path.remove(start)
            return path
        # calculate the valid neighbors
        vldneigh = getNeighbors(current)
        #print('Valid Neighbors for {} is {}'.format(current,vldneigh))

        for child in vldneigh:
            # checks in child is already in the closed set
            if child not in closedSet:
                fringe.append(child)
        path.append(current)
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
            elif(GRID[i] == 5):
                color = "yellow" # backtrack
            elif(GRID[i] ==6):
                color = "firebrick" #you're on fire
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
            elif(GRID[i] == 5):
                color = "yellow" #backtrack
            elif(GRID[i] ==6):
                color = "firebrick" #you're on fire
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
        window.after(400,window.destroy)
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


    tempNeighbors = [ up, down, left, right ] # all possible neighbors
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
