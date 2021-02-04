import random

print()  # prints a empty row

dim = int(input('Enter the size of the array: '))
prob = float(input('Enter the probability of an element being a 1 or 0: '))

grid = [ [1]*dim for n in range(dim)]
for row in grid:
    print(row)

numEmpty = (dim**2)*prob
numEmpty = int(round(numEmpty))
#print(numEmpty)

c = 0

while c < numEmpty :
    pos1 = random.randint(0,dim-1)
    pos2 = random.randint(0,dim-1)

    temp = grid[pos1][pos2]

    if (temp == 1):
        grid[pos1][pos2] = 0
        c +=1


print() #prints an empty row

for row in grid:
    print(row)

    



print() #prints an empty row