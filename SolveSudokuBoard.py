from math import sqrt

##board = [
##    [0, 15, 0, 1, 0, 2, 10, 14, 12, 0, 0, 0, 0, 0, 0, 0],
##    [0, 6, 3, 16, 12, 0, 8, 4, 14, 15, 1, 0, 2, 0, 0, 0],
##    [14, 0, 9, 7, 11, 3, 15, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
##    [4, 13, 2, 12, 0, 0, 0, 0, 6, 0, 0, 0, 0, 15, 0, 0,],
##    [0, 0, 0, 0, 14, 1, 11, 7, 3, 5, 10, 0, 0, 8, 0, 12],
##    [3, 16, 0, 0, 2, 4, 0, 0, 0, 14, 7, 13, 0, 0, 5, 15],
##    [11, 0, 5, 0, 0, 0, 0, 0, 0, 9, 4, 0, 0, 6, 0, 0],
##    [0, 0, 0, 0, 13, 0, 16, 5, 15, 0, 0, 12, 0, 0, 0, 0],
##    [0, 0, 0, 0, 9, 0, 1, 12, 0, 8, 3, 10, 11, 0, 15, 0],
##    [2, 12, 0, 11, 0, 0, 14, 3, 5, 4, 0, 0, 0, 0, 9, 0],
##    [6, 3, 0, 4, 0, 0, 13, 0, 0, 11, 9, 1, 0, 12, 16, 2],
##    [0, 0, 10, 9, 0, 0, 0, 0, 0, 0, 12, 0, 8, 0, 6, 7],
##    [12, 8, 0, 0, 16, 0, 0, 10, 0, 13, 0, 0, 0, 5, 0, 0],
##    [5, 0, 0, 0, 3, 0, 4, 6, 0, 1, 15, 0, 0, 0, 0, 0],
##    [0, 9, 1, 6, 0, 14, 0, 11, 0, 0, 2, 0, 0, 0, 10, 8],
##    [0, 14, 0, 0, 0, 13, 9, 0, 4, 12, 11, 8, 0, 0, 2, 0]
##
##]

#BOX_DIVISOR = int(sqrt(len(board[0])))

# returns a flipped version of the board
def GetFlipedBoard(grid):
    CRboard = []
    for r in range(len(grid)):
        temp = []
        for c in range(len(grid)):
            temp.append(grid[c][r])
        CRboard.append(temp)
    return CRboard

#CRboard = GetFlipedBoard(board)

# Check row for num and return false if num is in that row
def NotInRow(grid, num, cordinate):
    for i in range(len(grid[0])):
         if if grid[cordinate[0]][i] == num and cordinate[1] != i: 
            return False
    return True

# Check column for num and return false if num is in that column
def NotInCol(grid,num,cordinate):
    for i in range(len(grid)):
        if grid[i][cordinate[1]] == num and cordinate[0] != i:
            return False
    return True


# Check box for num and return false if num is in that row
def NotInBox(grid,num,cordinate):
    BOX_DIVISOR = int(sqrt(len(grid[0])))
    
    # Gets number of Boxes in any given row or column
    posBoxCordinate_X = cordinate[1] // BOX_DIVISOR
    posBoxCordinate_Y = cordinate[0] // BOX_DIVISOR


    # i loops from first box column to end column cordinate
    for i in range(posBoxCordinate_Y * BOX_DIVISOR, posBoxCordinate_Y * BOX_DIVISOR + BOX_DIVISOR):
        # j loops from first box row to end row cordinate
        for j in range(posBoxCordinate_X * BOX_DIVISOR, posBoxCordinate_X * BOX_DIVISOR + BOX_DIVISOR):
            if grid[i][j] == num and (i,j) != cordinate:
                return False

    return True


# returns true is num is a valid entry meaning there is no duplicates of that number in the row, column or box of its given position
# cordinate is a touple that holds the position being looked at (X, Y) cordinate
def IsValidNumber(grid, CRboard, num, cordinate):

    return(NotInRow(grid,num,cordinate) and NotInCol(grid,num,cordinate) and NotInBox(grid,num,cordinate))
            


# Finds the next empty box
def GetNextEmpty(grid):

    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == 0:
                return (i, j)  # row, col
    return False
  

# recursive function that runs until the sudoko board is solved then returns true
def GetSolution(grid, CRboard):
    
    find = GetNextEmpty(grid)
    if not find:
        return True
    
    else:
        row, col = find
        
    # iterates through all the numbers that couold fill a box
    for i in range(1,len(grid)+1):
        if i not in grid[row] and i not in CRboard[col]:
            if IsValidNumber(grid,CRboard,i,(row,col)):
                grid[row][col] = i
                CRboard[col][row] = i

                # recursive call
                if GetSolution(grid, CRboard):
                    return True
                
            
            grid[row][col] = 0
            CRboard[col][row] = 0

    return False


# display board. used for testing
##def Display(grid):
##
##    for i in range(len(grid)):
##        if i % BOX_DIVISOR == 0 and i != 0:
##            print()
##
##        for j in range(len(grid)):
##            if j % BOX_DIVISOR == 0 and j != 0:
##                print("   ", end="")
##                
##            if j == len(grid)-1:
##                print(grid[i][j])
##
##            else:
##                print(str(grid[i][j]) + " ", end="")



##print("UNSOLVED: \n")
##Display(board)
##GetSolution(board, CRboard)
##print("\nSOLVED: \n")
##Display(board)

