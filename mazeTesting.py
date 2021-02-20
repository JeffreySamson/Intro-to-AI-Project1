from tkinter import *
from typing import TYPE_CHECKING
import numpy as np
import random
import math
from queue import Empty, PriorityQueue
import heapq
from collections import deque
import time


# 0: blocked
#1: avaliable block
# -1: start
# -2: end
# -3: maze fire
# 5: move back
# 2 double move back
# 6: on fire
# 7: path

def main():
    
    # Declaring global variables 
    global SIZE     # Total size of the maze (Length of the array used to represent the maze)
    global DIM      # Dimension of the maze to make a n x n maze.
    global GRID     # Array object used to represent the maze.
    global PROB     # Probability of a space in the maze being an obstacle
    global start    # Starting point the agent travels from
    global end      # End goal that the agent must reach
    global q    # flammability rate

    DIM = 260
    SIZE = DIM**2
    PROB = 0.3
    start = 0
    end = SIZE-1
    makeGrid()

    start_time = time.time()
    path = BFS(start, end)
    #print(path)
    bfsTime = time.time() - start_time
    
    '''makeGrid()
    start_time = time.time()
    path = DFS(start, end)
    dfsTime = time.time() - start_time'''
    #makeGrid()
    #start_time = time.time()
    #path = AStar(start, end)
    #astarTime = time.time() - start_time

    '''astarTime = 0.0
    increment = 10
    times = [ ]
    while(astarTime < 60.0):
        DIM += increment
        makeGrid()
        start_time = time.time()
        BFS(start, end)
        astarTime = time.time() - start_time
        if astarTime > 61:
            increment = increment / 2
            DIM = DIM / 2
            continue
        times.append(astarTime)
    '''
    
    #print("--- DFS Finished in {} seconds ---".format(dfsTime))
    print("--- BFS Finished in {} seconds ---".format(bfsTime))
    #print("--- AStar Finsihed in {} seconds ---".format(times[len(times)-1]))

    # Initializing variables with user input through command line
    """DIM = int(input('Enter the size of the array: \n'))
    PROB = float(input('Enter the probability of an element between 1 or 0 (Not including 0): \n'))

    # Ensures that the probaility must be at least a 0 and less than 1
    while (PROB <0 or PROB >=1):
        print ('PROB must be between 1 and 0 (Not including 0 or 1)')
        PROB = float(input('Enter the probability of an element between 1 or 0 (Not including 0 or 1): \n'))

    # Initializing the flammability rate 
    q = 0
    # Initializing the size based on user input for dimensions.
    SIZE = DIM**2

    # Asks users if they want random start and end points and generates start and end points
    startEnd = input('Random start and end locations? (Y or N): \n').casefold().strip()
    # Checks for unacceptable answers
    while (startEnd != 'y' and startEnd != 'n'):
        print('Please enter Y or N')
        startEnd = input('Random start and end locations? (Y or N): \n')
    if (startEnd == 'y'):
        start = random.randint(0,SIZE-1)
        end = random.randint(0,SIZE-1)
        while (end == start):
            end = random.randint(0,SIZE-1) # check so that start and end is not the same 
    else:
        start = 0
        end = SIZE - 1

    # Print statement to let the user know what the start and end points are.
    print("Going from {} -> {}\n".format(start,end) ) 

    # Starts a while loop to get user input on what type of search they would like to execute
    exit = False
    while not exit:
        searchOrStrat = (input('Would you like to see a search type or strategy? (enter 1 for search type and 2 for strategy) \n')).strip()
        if searchOrStrat == '1':

            #makes the Grid and also make sure there is a solution
            makeGrid()
            solution = AStar(start,end)
            while (not solution):
                makeGrid()
                solution = AStar(start,end)
            searchType = input('Enter which search type you would like to use (enter 1 = BFS, 2 = DFS, 3 = Astar): \n').strip()
            # Executes the right method based on the user input and exits the while loop
            if searchType == "1":
                path = BFS(start,end)
                paintGRID(path)
                exit = True
                
            elif searchType == "2":
                path = DFS(start,end)
                paintGRID(path)
                exit = True

            elif searchType == "3":
                path = AStar(start,end)
                paintGRID(path)
                exit = True
            # Case for invalid user input
            else: print("Please enter 1, 2, or 3.\n")

        elif searchOrStrat == '2':
            # Asks for a flammability rate
            q = float(input('Enter the flammability rate: \n'))
            # Ensures the rate is at least a 0 and at most a 1
            while (q <0 or q >1):
                print ('Flammability rate must be between 1 and 0')
                q = float(input('Enter the flammability rate: \n'))

            strat = input("Which strategy would you like to execute? (Enter 1, 2, or 3)\n").strip()

            # creates the maze and makes sure that there is a path from fire to maze and there is a solution
            checkGrid()

            if strat == "1":
                path = strategy1(start,end)
                exit = True

            elif strat == "2":
                path = strategy2(start,end)
                exit = True

            elif strat == "3":
                path = strategy3(start,end)
                exit = True
            else:
                print("Please enter 1, 2, or 3.\n")
                
        else: print("Please enter 1, 2, or 3.\n")

"""
    print()

######################[problems]######################

# Method that determines if a path between two points is possible by using DFS 
def problem2():
    global DIM
    global PROB
    i = 0
    k = 0
    iterations = 100
    result = [0] * 20
    while i < 1:
        PROB = float(str(round(i, 2)))
        print(PROB)
        result[k] = 0
        for j in range(iterations):
            makeGrid()
            if (DFS(start, end)):
                result[k] = result[k] + 1
        k = k + 1
        i = i + 0.05
    print("Dimension size is", DIM, "and there were", iterations, "iterations done")
    print(result)

# Method that executes all three strategies on the same maze and compares the results
def problem6():
    global GRID
    global DIM
    global PROB
    global q
    i = 0
    k = 0
    #PROB = 0.3
    iterations = 30
    result1 = [0] * 20
    result2 = [0] * 20
    result3 = [0] * 20
    while i <= 1:
        q = float(str(round(i, 2)))
        print(q)
        result1[k] = 0
        result2[k] = 0
        result3[k] = 0
        for j in range(iterations):
            checkGrid()
            copyMaze = np.copy(GRID)

            if (strategy1(start, end)):
                result1[k] = result1[k] + 1
            GRID = np.copy(copyMaze)
            if (strategy2(start, end)):
                result2[k] = result2[k] + 1
            GRID = np.copy(copyMaze)
            if (strategy3(start, end)):
                result3[k] = result3[k] + 1
            GRID = np.copy(copyMaze)
        k = k + 1
        i = i + 0.05
    print("Dimension size is", DIM, "and there were", iterations, "iterations done")
    print("Strategy 1:", result1)
    print("Strategy 2:", result2)
    print("Strategy 3:", result3)

######################[functions]######################
# Method to determine the origin of the fire
def startFire():
    global GRID
    #Determines a random point to start the fire
    fireSeed = random.randint(0,SIZE-1) 

    # Checks for fire starting at start or end point
    while (GRID[fireSeed] == 0 or fireSeed == SIZE-1):
        fireSeed = random.randint(0,SIZE-1)
    # Changes array element to represent fire
    GRID[fireSeed] = -3

    return fireSeed

# Method that displays the colored maze
def paintGRID(path):
    global GRID

    showTempMaze()
  
    length = len(path)
    # fills in the colors for the maze 
    for i in range(length):
      if (i > 1) and (path[i] not in getNeighbors(path[i-1])) and (not i == (length-1) )  :
        backtrack = [path[i-1]] + AStar(path[i-1],path[i])
        for j in backtrack:
          if j == path[i-1]:
            temp = GRID[j]
            GRID[j] =  6
            showTempMaze()
            GRID[j] = temp

          GRID[j]= pickColor(j)
          showTempMaze()

      else:
        GRID[path[i]] = pickColor(path[i])
        showTempMaze()

      GRID[path[i]] = -2
    showMaze()
    return

# Method to execute strategy 3
def strategy3(start,end):
    global GRID
    # Checks if there is a path
    path = AStarMod(start,end) 
    # If there is no path, prints an error message
    if not path:
        print("strategy 3: No Solution")
        showMaze()
        return False

    current = start

    while not path[0] == end:
        path = AStarMod(current,end)

        if (not path):
            print("strategy 3: SORRY NO SAFE PATH!")
            showMaze()
            return False

        GRID[path[0]] = pickColor(path[0])
        current = path[0]
        showTempMaze()

        #Case for the agent reaching the goal state
        if current == end:
            print("strategy 3: MADE IT!")
            showTempMaze()
            GRID[end] = -2
            showMaze()
            return True

        advFireOneStep()
        showTempMaze()

        # Case for the agent catching on fire
        if (GRID[current] == -3):
            print("strategy 3: YOU'RE ON FIRE!")
            GRID[current] = 6
            showMaze()
            return False
    # Safeguard incase code exits while loop without returning a value
    print("strategy 3: MADE IT!")
    showTempMaze()
    GRID[end] = -2
    showMaze()
    return True

# Creates a new heuristic that takes into account the fire and it's neighbors
def heu2(current,end):

    global SIZE

    #euclidean distance
    dis = diagDis(current,end)

    # distance from fire 
    fire = diagDis(current,findFire(current))

    if fire <= 2:
        dis = dis + (SIZE-fire) + len(getFireNeighbors(current,GRID))

    return dis

# Method that INSERT DEF
def findFire(strt):

    global GRID


    # creates the stack that you have already visited
    closedSet = []

    # creates the fringe stack and adds start to fringe
    fringe = deque([(strt,[])])

    while fringe: # checks if the fringe is empty
        
        # current is the current node
        # path keeps track of the path taken to reach current from start
        # everything at the top of the queue will always be the shortest path
        current, path = fringe.popleft()
        closedSet.append(current)

        # found the path
        if (GRID[current] == -3):
            return current

        # calculate the valid neighbors
        vldneigh = getNeighbors(current) + getFireNeighbors(current,GRID)

        for child in vldneigh:
            if child not in closedSet:
                # new path is path + current for this child
                fringe.append((child,path + [current]))
                closedSet.append(child)

    return None

# Method that uses Astar search but also uses the diagonal distance to end goal and distance to fire as a weight in its decision
def AStarMod(start,end):
  
  dist = {}
  processed = {}
  prev = {}
    #Initializes the lists used
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
          return path
      # goes through the nodes that haven't been processed yet.
      if not processed[v]:
          vldneigh = getNeighbors(v)
          for u in vldneigh:
              if ((d + heu2(u,end)) < dist[u]):
                  dist[u] = d + heu2(u,end)
                  heapq.heappush(fringe,(dist[u],u,path + [u]))
                  prev[u] = v
          processed[v] = True
  return None

# Executes the AStar search algo to find fire
def AStarFire(start,end):
  
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
          return path
      if not processed[v]:
          vldneigh = getNeighbors(v) + getFireNeighbors(v,GRID)
          for u in vldneigh:
              if ((d + diagDis(u,end)) < dist[u]):
                  dist[u] = d + diagDis(u,end)
                  #print('going to {} from {} is {}'.format(v,u,dist[u]))
                  heapq.heappush(fringe,(dist[u],u,path + [u]))
                  prev[u] = v
          processed[v] = True
  return None

# Keeps track of current fire and creates a new path but never expects the future
def strategy2(start,end):

    global GRID

    path = AStar(start,end)

    if not path:
        print("strategy 2: No Solution")
        showMaze()
        return False

    current = start

    while not path[0] == end:
        
        path = AStar(current,end)


        if (not path):
            print("strategy 2: SORRY NO SAFE PATH!")
            showMaze()
            return False


        # guy moves
        GRID[path[0]] = pickColor(path[0])

        showTempMaze()

        current = path[0]

        if current == end:
            print("strategy 2: MADE IT!")
            showTempMaze()
            GRID[end] = -2
            showMaze()
            return True

        advFireOneStep()

        showTempMaze()

        if (GRID[current] == -3):
            print("strategy 2: YOU'RE ON FIRE!")
            GRID[current] = 6
            showMaze()
            return False

    print("strategy 2: MADE IT!")
    showTempMaze()
    GRID[end] = -2
    showMaze()
    return True

# Executes strategy1
def strategy1(start,end):

    global GRID
    path = AStar(start,end)

    if not path:
        print("strategy 1: No solution")
        showMaze()
        return False

    pathLength = len(path)
    #print(path)

    for current in range(pathLength):

        if (GRID[path[current]] == -3):
            print("strategy 1: YOU'RE ON FIRE!")
            GRID[path[current]] = 6
            showMaze()
            return False

        if path[current] == end:
            print("strategy 1: Made it!")
            GRID[end] = 7
            showTempMaze()
            GRID[end] = -2
            showMaze()
            return True

        #moves the guy forward
        GRID[path[current]] = pickColor(path[current])
        showTempMaze()

        # moves fire forward
        advFireOneStep()
        showTempMaze()

        # kills guy if he is currently on fire (== -3) or if his next move is on fire
        if (GRID[path[current]] == -3):
            print("strategy 1: YOU'RE ON FIRE!")
            GRID[path[current]] = 6
            showMaze()
            return False

    print("strategy 1: Made it!")
    GRID[end] = 7
    showTempMaze()
    GRID[end] = -2
    showMaze()
    return True

# Advances the fire by one step
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

# Executes the AStar search algo
def AStar(start,end):
  global GRID
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

# Eucledian heuristic for AStar
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

# Executes the BFS algorithm
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

# Executes the DFS algorithms
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
          path.remove(start)
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

# Method to determine the color of the GUI based on the elements value
def pickColor(current):

  global GRID

  if GRID[current] == 1:
    color = 7
  elif GRID[current] == 7:
    color = 5
  elif GRID[current] ==5:
    color = 2
  elif GRID[current] == 2:
    color = 3
  else: 
    color =7

  return color

# Makes the grid using the probability and the size
def makeGrid():
    global SIZE
    global PROB
    global GRID
    global start
    global end

    GRID = np.ones(DIM**2)

    GRID[start] = -1
    GRID[end] = -2
    print(SIZE)
    for i in range(SIZE):
        print(i)
        if  ( not i == start ) and (not i == end):
            if (random.random() <= PROB):
                GRID[i] =0

# Method that checks the maze and determines that there is a soloutio
def checkGrid():

    makeGrid()
    fireSeed = startFire()
    FirePath = AStarFire(start,fireSeed)
    solution = AStar(start,end)
    #print(solution)
    #print(FirePath)
    while (not FirePath) or  (not solution):
        makeGrid()
        fireSeed = startFire()
        FirePath = AStarFire(start,fireSeed)
        solution = AStar(start,end)


    return

# Makes the visual canvas for the grid
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
          elif(GRID[i] == 2):
              color = "hotpink" # double backtrack
          elif(GRID[i] == 3):
              color = "grey" # triple backtrack
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

# Psuedo animating the maze move
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
        elif(GRID[i] == 2):
            color = "hotpink" # double backtrack
        elif(GRID[i] == 3):
            color = "grey"  # triple backtrack
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
    time = DIM*50
    window.after(time,window.destroy)
    window.mainloop()

# Gets the left, right, up, and down neighbors in that order
def getNeighbors(current):

  global SIZE
  global GRID
  global DIM

  left = current -1
  right = current+1
  up = current - DIM
  down = current + DIM


  tempNeighbors = [ left, right, up, down ] # all possible neighbors
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

# Gets the Neighbors that are on fire
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