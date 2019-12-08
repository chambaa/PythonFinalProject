import pygame
from SolveSudokuBoard import GetSolution, IsValidNumber, GetNextEmpty, GetFlipedBoard
import time
from math import sqrt
pygame.font.init()

__author__ = "Klayton Hacker"
__email__ = "hackerkj@mail.uc.edu"

__author__ = "Anna Chambers"
__email__ = "chambaa@mail.uc.edu"


class Box: #individual boxes

    def __init__(self, board, row, col, width ,height):
        self.value = board[row][col]
        self.board = board
        self.temp = 0
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.isSelected = False

    def DrawBox(self, window):
        font = pygame.font.SysFont("comicsans", 40)

        gap = self.width / len(self.board[0])
        x = self.col * gap
        y = self.row * gap

        if self.temp != 0 and self.value == 0:
            text = font.render(str(self.temp), 1, (192,192,192))
            window.blit(text, (x+5, y+5))
            
        elif(self.value != 0): # fills in the starting and correct values
            text = font.render(str(self.value), 1, (255, 255, 255))
            window.blit(text, (x + (gap / 2 - text.get_width() / 2), y + (gap / 2 - text.get_height() / 2)))

        if self.isSelected: # makes a red boarder around the selected box
            pygame.draw.rect(window, (255,0,0), (x,y, gap ,gap), 3)

    def setValue(self, val):
        self.value = val

    def setTemp(self, val):
        self.temp = val



class Grid: #Full board
    
    def __init__(self, board, solvedBoard, BOX_DIVISOR, width, height):
        self.board = board
        self.solvedBoard = solvedBoard
        self.BOX_DIVISOR = BOX_DIVISOR
        self.width = width
        self.height = height
        self.rows = len(self.board[0])
        self.cols = len(self.board[0])
        self.boxes = [[Box(self.board, i, j, width, height) for j in range(self.cols)] for i in range(self.rows)]
        self.UserBoard = None
        self.CoorSelected = None

    def UpdateUserBoard(self):
        self.UserBoard = [[self.boxes[i][j].value for j in range(self.cols)] for i in range(self.rows)]

    def WasValuePlaced(self, val):
        row, col = self.CoorSelected
        if self.boxes[row][col].value == 0:
            self.boxes[row][col].setValue(val)
            self.UpdateUserBoard()

            if self.solvedBoard[row][col] == val:
                return True
            else:
                self.boxes[row][col].setValue(0)
                self.boxes[row][col].setTemp(0)
                self.UpdateUserBoard()
                return False

    def PlaceTemp(self, val):
        row, col = self.CoorSelected
        self.boxes[row][col].setTemp(val)

    def DrawGrid(self, window):
        # Grid Lines
        gap = self.width / (self.BOX_DIVISOR ** 2)
        for i in range(self.rows + 1):
            if i % self.BOX_DIVISOR == 0 and i != 0:
                thick = 4
            else:
                thick = 1
            pygame.draw.line(window, (255,255,255), (0, i * gap), (self.width, i * gap), thick)
            pygame.draw.line(window, (255, 255, 255), (i * gap, 0), (i * gap, self.height), thick)

        # Boxes
        for i in range(self.rows):
            for j in range(self.cols):
                self.boxes[i][j].DrawBox(window)

    def SelectBox(self, row, col):
        # Reset previously selected
        for i in range(self.rows):
            for j in range(self.cols):
                self.boxes[i][j].isSelected = False

        # set new selected
        self.boxes[row][col].isSelected = True
        self.CoorSelected = (row, col)


    def PositionOfClick(self, pos): 
        # Returns the coordinates of what square the user clicks on
        if pos[0] < self.width and pos[1] < self.height:
            gap = self.width / (self.BOX_DIVISOR ** 2)
            x = pos[0] // gap
            y = pos[1] // gap
            return (int(y),int(x))
        else:
            return None

    def isFinished(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.boxes[i][j].value == 0:
                    return False
        return True



##

def SetTime(secs):
    sec = secs % 60
    minute = secs // 60
    hour = minute // 60

    if(hour == 0):
        mat = " " + str(minute) + ":" + str(sec)
    else:
        mat = " " + str(hour) + ":" + str(minute) + ":" + str(sec)
    return mat

def UpdateScreen(window, board, time, strikes):
    window.fill((0,0,0))
    # Draw time
    fnt = pygame.font.SysFont("comicsans", 30)
    text = fnt.render("Time: " + SetTime(time), 1, (255,255,255))
    window.blit(text, (540 - 160, 560))
    # Draw Strikes
    text = fnt.render(str(3 - strikes) + " strikes remaining:", 1, (255, 255, 255))
    window.blit(text, (20, 560))
    
    text = fnt.render("X " * strikes, 1, (255, 0, 0))
    window.blit(text, (230, 560))
    # Draw grid and board
    board.DrawGrid(window)

##

def main():
    board1 = [

    [0,0,0,0],
    [0,0,1,0],
    [4,0,0,0],
    [0,2,0,3],

]
    TempBoard1 = [

    [0,0,0,0],
    [0,0,1,0],
    [4,0,0,0],
    [0,2,0,3],

]
    board2 = [

    [7,8,0,4,0,0,1,2,0],
    [6,0,0,0,7,5,0,0,9],
    [0,0,0,6,0,1,0,7,8],
    [0,0,7,0,4,0,2,6,0],
    [0,0,1,0,5,0,9,3,0],
    [9,0,4,0,6,0,0,0,5],
    [0,7,0,3,0,0,0,1,2],
    [1,2,0,0,0,7,4,0,0],
    [0,4,9,2,0,6,0,0,7]

]
    TempBoard2 = [

    [7,8,0,4,0,0,1,2,0],
    [6,0,0,0,7,5,0,0,9],
    [0,0,0,6,0,1,0,7,8],
    [0,0,7,0,4,0,2,6,0],
    [0,0,1,0,5,0,9,3,0],
    [9,0,4,0,6,0,0,0,5],
    [0,7,0,3,0,0,0,1,2],
    [1,2,0,0,0,7,4,0,0],
    [0,4,9,2,0,6,0,0,7]

]
    
    board3 = [
    [0, 15, 0, 1, 0, 2, 10, 14, 12, 0, 0, 0, 0, 0, 0, 0],
    [0, 6, 3, 16, 12, 0, 8, 4, 14, 15, 1, 0, 2, 0, 0, 0],
    [14, 0, 9, 7, 11, 3, 15, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
    [4, 13, 2, 12, 0, 0, 0, 0, 6, 0, 0, 0, 0, 15, 0, 0,],
    [0, 0, 0, 0, 14, 1, 11, 7, 3, 5, 10, 0, 0, 8, 0, 12],
    [3, 16, 0, 0, 2, 4, 0, 0, 0, 14, 7, 13, 0, 0, 5, 15],
    [11, 0, 5, 0, 0, 0, 0, 0, 0, 9, 4, 0, 0, 6, 0, 0],
    [0, 0, 0, 0, 13, 0, 16, 5, 15, 0, 0, 12, 0, 0, 0, 0],
    [0, 0, 0, 0, 9, 0, 1, 12, 0, 8, 3, 10, 11, 0, 15, 0],
    [2, 12, 0, 11, 0, 0, 14, 3, 5, 4, 0, 0, 0, 0, 9, 0],
    [6, 3, 0, 4, 0, 0, 13, 0, 0, 11, 9, 1, 0, 12, 16, 2],
    [0, 0, 10, 9, 0, 0, 0, 0, 0, 0, 12, 0, 8, 0, 6, 7],
    [12, 8, 0, 0, 16, 0, 0, 10, 0, 13, 0, 0, 0, 5, 0, 0],
    [5, 0, 0, 0, 3, 0, 4, 6, 0, 1, 15, 0, 0, 0, 0, 0],
    [0, 9, 1, 6, 0, 14, 0, 11, 0, 0, 2, 0, 0, 0, 10, 8],
    [0, 14, 0, 0, 0, 13, 9, 0, 4, 12, 11, 8, 0, 0, 2, 0]

]
    TempBoard3 = [
    [0, 15, 0, 1, 0, 2, 10, 14, 12, 0, 0, 0, 0, 0, 0, 0],
    [0, 6, 3, 16, 12, 0, 8, 4, 14, 15, 1, 0, 2, 0, 0, 0],
    [14, 0, 9, 7, 11, 3, 15, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
    [4, 13, 2, 12, 0, 0, 0, 0, 6, 0, 0, 0, 0, 15, 0, 0,],
    [0, 0, 0, 0, 14, 1, 11, 7, 3, 5, 10, 0, 0, 8, 0, 12],
    [3, 16, 0, 0, 2, 4, 0, 0, 0, 14, 7, 13, 0, 0, 5, 15],
    [11, 0, 5, 0, 0, 0, 0, 0, 0, 9, 4, 0, 0, 6, 0, 0],
    [0, 0, 0, 0, 13, 0, 16, 5, 15, 0, 0, 12, 0, 0, 0, 0],
    [0, 0, 0, 0, 9, 0, 1, 12, 0, 8, 3, 10, 11, 0, 15, 0],
    [2, 12, 0, 11, 0, 0, 14, 3, 5, 4, 0, 0, 0, 0, 9, 0],
    [6, 3, 0, 4, 0, 0, 13, 0, 0, 11, 9, 1, 0, 12, 16, 2],
    [0, 0, 10, 9, 0, 0, 0, 0, 0, 0, 12, 0, 8, 0, 6, 7],
    [12, 8, 0, 0, 16, 0, 0, 10, 0, 13, 0, 0, 0, 5, 0, 0],
    [5, 0, 0, 0, 3, 0, 4, 6, 0, 1, 15, 0, 0, 0, 0, 0],
    [0, 9, 1, 6, 0, 14, 0, 11, 0, 0, 2, 0, 0, 0, 10, 8],
    [0, 14, 0, 0, 0, 13, 9, 0, 4, 12, 11, 8, 0, 0, 2, 0]

]
    
    window = pygame.display.set_mode((540,600)) #set the size of the window
    pygame.display.set_caption("Sudoku") #top caption

    
    dif = int(input("Enter Difficulty (1,2,3): "))
    
    if(dif == 1):
        BOX_DIVISOR = int(sqrt(len(board1[0])))
        GetSolution(TempBoard1,GetFlipedBoard(TempBoard1))
        board = Grid(board1, TempBoard1, BOX_DIVISOR, 540, 540)
        
        
    elif(dif == 2):
        BOX_DIVISOR = int(sqrt(len(board2[0])))
        GetSolution(TempBoard2,GetFlipedBoard(TempBoard2))
        board = Grid(board2, TempBoard2,BOX_DIVISOR, 540, 540)
        

    elif(dif == 3):
        print("Must wait 5 minutes for the computer to solve the board...")
        BOX_DIVISOR = int(sqrt(len(board3[0])))
        GetSolution(TempBoard3,GetFlipedBoard(TempBoard3))
        board = Grid(board3, TempBoard3,BOX_DIVISOR, 540, 540)
        

        
    else:
        print("Enter a number 1-3")

    key = None
    run = True
    start = time.time()
    strikes = 0
    while run:

        gameTime = round(time.time() - start)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                clicked = board.PositionOfClick(pos)
                if clicked:
                    board.SelectBox(clicked[0], clicked[1])
                    key = None
                    current_string = ""
                    
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_0:
                    current_string += "0"
                    key = int(current_string)
                if event.key == pygame.K_1:
                    current_string += "1"
                    key = int(current_string)
                if event.key == pygame.K_2:
                    current_string += "2"
                    key = int(current_string)
                if event.key == pygame.K_3:
                    current_string += "3"
                    key = int(current_string)
                if event.key == pygame.K_4:
                    current_string += "4"
                    key = int(current_string)
                if event.key == pygame.K_5:
                    current_string += "5"
                    key = int(current_string)
                if event.key == pygame.K_6:
                    current_string += "6"
                    key = int(current_string)
                if event.key == pygame.K_7:
                    current_string += "7"
                    key = int(current_string)
                if event.key == pygame.K_8:
                    current_string += "8"
                    key = int(current_string)
                if event.key == pygame.K_9:
                    current_string += "9"
                    key = int(current_string)
                    
                if event.key == pygame.K_RETURN:
                    key = int(current_string)
                    i, j = board.CoorSelected
                    
                    if board.boxes[i][j].temp != 0:
                        
                        if not board.WasValuePlaced(board.boxes[i][j].temp):
                            print("Wrong Number. Try Again.")
                            strikes += 1
                            key = None
                            current_string = ""
                            
                        if board.isFinished():
                            print("YOU WIN")
                            run = False
                            
                        if strikes == 3:
                            print("YOU LOSE")
                            run = False

        if board.CoorSelected and key != None:
            board.PlaceTemp(key)

        UpdateScreen(window, board, gameTime, strikes)
        pygame.display.update()


main()
pygame.quit()
