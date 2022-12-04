from tkinter import *
from model import Model
from view import View
import pandas as pd

class Controller:
    # Initialize the controller object
    # @param textbased - if the game is textbased
    # @param diff - the difficulty of the game 
    def __init__(self, textbased, diff):    
        
        isTesting = input("Enter testing mode? (Y, N): ").lower()
        
        # sets testing mode
        self.testing = True if isTesting == 'y' else False
        if self.testing:
            self.mineCoords = []
            self.tresureCoords = []
            self.testingMode()
            
        # set the difficulty of the game and update the number of mines
        self.numMines = 0
        self.setDiff(diff)
        
        self.textbased = textbased
        
        # initialize the view and model
        self.view = View(self)
        self.model = Model(self, self.numMines, self.testing)
        
        # init the timer for non textbased game
        if not self.textbased:
            self.view.updateTimer() # init timer
     
        self.view.refreshLabels()
    
    def testingMode(self):
        filename = input("Enter file name for CSV file: ")
        self.customBoard = pd.read_csv(filename + ".csv", header=None)
        # check board if valid
        eachRow = True
        eachColumn = True
        numAdjacent = 0
        isolated = False
        for x in range(0, 8):
            if 1 not in self.customBoard[x]:
                eachRow = False
            foundMine = False
            for y in range(0, 8):
                if self.customBoard[x][y] == 2:
                    self.tresureCoords.append({"x":y, "y":x})
                if self.customBoard[x][y] == 1:
                    self.mineCoords.append({"x":y, "y":x})
                    foundMine = True
                    # check if same row and column exists
                    coords = self.coordsHelper(x, y)
                    isoCoords = self.coordsHelper(x, y, True)
                    for n in coords:
                        try:
                            if self.customBoard[n["x"]][n["y"]] == 1:
                                numAdjacent += 1   
                        except KeyError:
                            pass
                    isoMineCount = 0
                    for n in isoCoords:
                        try:
                            if self.customBoard[n["x"]][n["y"]] == 1:
                                isoMineCount += 1
                        except KeyError:
                            pass
                    if isoMineCount == 0:
                        isolated = True
            if foundMine == False:
                eachColumn = False
        
        if not eachRow and not eachColumn and numAdjacent != 0 and not isolated:
            # not valid
            print("CSV file is invalid")
            self.__init__()
    
    def coordsHelper(self, j, k, iso=False):
        if iso:
            coords = [
            {"x": j-1,  "y": k-1},  #top right
            {"x": j-1,  "y": k},    #top middle
            {"x": j-1,  "y": k+1},  #top left
            {"x": j,    "y": k-1},  #left
            {"x": j,    "y": k+1},  #right
            {"x": j+1,  "y": k-1},  #bottom right
            {"x": j+1,  "y": k},    #bottom middle
            {"x": j+1,  "y": k+1},  #bottom left
            {"x": j-2,  "y": k-2},
            {"x": j-2,  "y": k},  
            {"x": j-2,  "y": k+2},
            {"x": j,    "y": k-2},
            {"x": j,    "y": k+2},
            {"x": j+2,  "y": k-2},
            {"x": j+2,  "y": k},  
            {"x": j+2,  "y": k+2},
            {"x": j-2,  "y": k+1}, 
            {"x": j+2,  "y": k+1}, 
            {"x": j-2,  "y": k-1}, 
            {"x": j+2,  "y": k-1}, 
            {"x": j+1,  "y": k+2}, 
            {"x": j-1,  "y": k+2}, 
            {"x": j+1,  "y": k-2}, 
            {"x": j+1,  "y": k-2}, 
        ]
        else:
            coords = [
                {"x": j-1,  "y": k},    #top
                {"x": j,    "y": k-1},  #left
                {"x": j,    "y": k+1},  #right
                {"x": j+1,  "y": k},    #bottom
            ]
        return coords
    
    # sets the difficutly for the game
    # @Requires("typeOf(diff) == 'string'", "diff != None")
    # @Ensures("self.SIZE_X != None", "self.SIZE_Y != None", "self.numMines != None", 
    #           "self.SIZE_X == 8 or self.SIZE_X == 16 or self.SIZE_X == 30", 
    #           "self.SIZE_Y == 8 or self.SIZE_Y == 16", "self.numMines == 10 or self.numMines == 40 or self.numMines == 99")
    # 
    def setDiff(self, diff):
        if diff == "beginner":
            self.SIZE_X = 8
            self.SIZE_Y = 8
            self.numMines = 10
        elif diff == "intermediate":    
            self.SIZE_X = 16
            self.SIZE_Y = 16
            self.numMines = 40
        else:
            self.SIZE_X = 30
            self.SIZE_Y = 16
            self.numMines = 99
    
    # restarts the game
    def restart(self):
        #  start new game
        self.model = Model(self, self.numMines, self.testing)
        self.view.restart()
    
    # starts the loop for the game 
    # 
    # this method is moved from the main method of the orignial game to the controller class because it is controlling the starting of the game
    def startGame(self):
        if self.textbased:
            while (not self.model.gameEnd):
                self.view.displayBoard()
                self.view.getNextMove()
        else:
            self.view.tk.mainloop()
        
    # displays all of the mines and treasure on the board after gameOver
    # 
    # this method is moved to the controller clas because it is controlling what method is called for the next part of the game
    def checkMine(self):
        for x in range(0, self.SIZE_X):
            for y in range(0, self.SIZE_Y):
                if self.model.tiles[x][y]["isMine"] == False and self.model.tiles[x][y]["state"] == self.model.STATE_FLAGGED:
                    self.view.updateButton(self.model.tiles[x][y], "wrong")
                if self.model.tiles[x][y]["isMine"] == True and self.model.tiles[x][y]["state"] != self.model.STATE_FLAGGED:
                    self.view.updateButton(self.model.tiles[x][y], "mine")
                if self.model.tiles[x][y]["isTreasure"] == True:
                    self.view.updateButton(self.model.tiles[x][y], "treasure")
        if not self.textbased:
            self.view.tk.update()
    
    # quits the game
    # 
    # this method is in the controlle class because it decides what method to call the game is quit
    def quit(self):
        if not self.textbased:
            self.view.tk.quit()