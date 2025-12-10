grid = [[None] * 20 for j in range(18) ]
print(grid)

grid[1][1] = "X"
grid[2][3] = "X"


print("Matrice:")
for i in range(0,19,1):
    
    for j in range(0,17,1):
        if grid[j][i] is None:
            print("0",end=" ")
        else:
            print("X",end=" ")
    print("||")