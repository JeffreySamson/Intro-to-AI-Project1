
from tkinter import *
import numpy as np
import random


DIM = int(input('Enter the size of the array: '))
PROB = float(input('Enter the probability of an element being a 1 or 0: '))
while PROB <0 or PROB >1:
    print ('PROB must be between 1 and 0')
    PROB = float(input('Enter the probability of an element being a 1 or 0: '))
SIZE = DIM**2
GRID = np.ones(DIM**2)

def makeGrid():
    numEmpty = (SIZE)*PROB
    numEmpty = int(round(numEmpty))

    c = 0
    while c < numEmpty :
        temp = random.randint(0,SIZE-1)

        if (GRID[temp] == 1):
            GRID[temp] = 0
            c +=1

class checkerBoard():
    def __init__(self):
        window = Tk()
        window.title("Fire Maze")

        for i in range(SIZE):
            if(GRID[i] == 1):
                color = "white"
            else :
                color = "black"
            Canvas(window, width=50, height = 50, bg = color).grid(row = i // DIM, column = i % DIM)
        window.mainloop()
        


makeGrid()
checkerBoard()
def findNeighbors(index):