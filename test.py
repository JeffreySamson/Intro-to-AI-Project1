from tkinter import *
from typing import TYPE_CHECKING
import numpy as np
import random
import math
from queue import Empty, PriorityQueue
import heapq
from collections import deque

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
    # hello
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

    DIM = 10
    PROB = 0
    q = 0.1

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


    #solution = DFS(start,end)

    # checks if there is a solution and then marks the path

    #strategy3(start,end)

    print() #prints an empty line
    # generates the final solution

    #mazeCopy = np.copy(GRID)

    '''makeGrid()

    empty = SIZE - sum(GRID) -5

    while (not empty == PROB*SIZE) or (not AStar(start,end)):
        makeGrid()
        empty = SIZE - sum(GRID) -5

    
    showMaze()'''

    #GRID = mazeCopy

    #showMaze()
    #strategy3(start,end)
    #problem2()
    checkGrid()

    problem6()
    #showMaze()
    print()

######################[problems]######################
def problem2():
    global DIM
    global PROB
    i = 0
    k = 0
    iterations = 100
    result = [0] * 20
    while i < 1:
        PROB = i
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

def problem6():
    global DIM
    global PROB
    global q
    i = 0
    k = 0
    PROB = 0.3
    iterations = 10
    result1 = [0] * 20
    result2 = [0] * 20
    result3 = [0] * 20
    while i < 1:
        q = i
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
def startFire():

  global GRID

  fireSeed = random.randint(0,SIZE-1)

  # fire can't start at the beginning or end
  while (GRID[fireSeed] == 0 or fireSeed == SIZE-1):
      fireSeed = random.randint(0,SIZE-1)

  GRID[fireSeed] = -3

  return fireSeed

def paintGRID(path):

  global GRID

  showTempMaze()
  
  length = len(path)

  for i in range(length):

    #print(f"{path[i]} has neighbors {getNeighbors(path[i])}")

    if (i>1 and (path[i] not in getNeighbors(path[i-1]) ) ) :


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

  return

def strategy3(start,end):


  global GRID

  path = AStarMod(start,end)

  if not path:
      print("No Solution")
      return

  current = start

  while not path[0] == end:
      
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


      #showTempMaze()
  

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

def findFire(strt):

    global GRID


    # creats the stack that you have already visited
    closedSet = []

    # creates the fringe stack and adds start to fringe
    fringe = deque([(strt,[])])

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

#executes the AStar search algo to find fire
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
          #print ("Success!")
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

  #print("No path")
  return None

# keeps track of current fire and creates a new path but never expects the future
def strategy2(start,end):

  global GRID

  path = AStar(start,end)

  if not path:
      print("No Solution")
      return

  current = start

  while not path[0] == end:
      
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


      #showTempMaze()
  

  print("MADE IT!")
  return

# executes strategy1
def strategy1(start,end):

  global GRID
  path = AStar(start,end)
  
  if not path:
      print("No solution")
      return

  pathLength = len(path)
  #print(path)

  for current in range(pathLength):

      if (GRID[path[current]] == -3):
          print("Stragie: YOU'RE ON FIRE!")
          GRID[path[current]] = 6
          showMaze()
          return

      if path[current] == end:
          print("Made it!")
          return

      #moves the guy forward
      GRID[path[current]] = pickColor(path[current])

      # moves fire forward
      advFireOneStep()

      # kills guy if he is currently on fire (== -3) or if his next move is on fire
      if (GRID[path[current]] == -3):
          print("YOU'RE ON FIRE!")
          GRID[path[current]] = 6
          showMaze()
          return
      
      # shows the maze
      #showTempMaze()

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

# makes the grid using the probability and the size
def makeGrid():
    global SIZE
    global PROB
    global GRID
    global start
    global end

    GRID = np.ones(DIM**2)

    GRID[start] = -1
    GRID[end] = -2

    for i in range(SIZE):
        if  ( not i == start ) and (not i == end):
            if (random.random() <= PROB):
                GRID[i] =0

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
    window.after(600,window.destroy)
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