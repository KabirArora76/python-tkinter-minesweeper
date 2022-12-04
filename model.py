# from tkinter import *
# from tkinter import messagebox as tkMessageBox
from collections import deque
import random
import platform
import time
from datetime import time, date, datetime

class Model:
    def __init__(self, controller, numMines, testing):
        
        self.controller = controller
        
        # create flag and clicked tile variables
        self.flagCount = 0
        self.correctFlagCount = 0
        self.clickedCount = 0
        self.STATE_DEFAULT = 0
        self.STATE_CLICKED = 1
        self.STATE_FLAGGED = 2
        self.gameEnd = False
        
        # create buttons
        self.tiles = dict({})
        self.mines = numMines
        self.treasures = 0
        self.treasureCredit = 0
        for x in range(0, self.controller.SIZE_X):
            for y in range(0, self.controller.SIZE_Y):
                if y == 0:
                    self.tiles[x] = {}

                id = str(x) + "_" + str(y)
                isMine = False
                isTreasure = False

                # # currently random amount of mines
                # if random.uniform(0.0, 1.0) < 0.1:
                #     isMine = True
                #     self.mines += 1
                
                tile = {
                    "id": id,
                    "isMine": isMine,
                    "isTreasure": isTreasure,
                    "state": self.STATE_DEFAULT,
                    "coords": {
                        "x": x,
                        "y": y
                    },
                    "button": self.controller.view.makeButton("plain"),
                    "mines": 0 # calculated after grid is built
                }
                
                if not controller.textbased:
                    self.controller.view.bindButton(tile, x, y)

                self.tiles[x][y] = tile
                
        self.placeMines(self.mines, testing)
        
        # loop again to find nearby mines and display number on tile
        for x in range(0, self.controller.SIZE_X):
            for y in range(0, self.controller.SIZE_Y):
                mc = 0
                for n in self.getNeighbors(x, y):
                    mc += 1 if n["isMine"] else 0
                self.tiles[x][y]["mines"] = mc
        
        self.placeTreasure(self.mines, testing)
    
    # this method randoly places a specific number of mines on the board
    # 
    # this method is in the model class because it a core element of the game
    def placeMines(self, numMines, testing):
        if testing:
            for n in self.controller.mineCoords:
                self.tiles[n["x"]][n["y"]]["isMine"] = True
        else:
            for i in range(numMines):
                x = random.randint(0, self.controller.SIZE_X-1)
                y = random.randint(0, self.controller.SIZE_Y-1)
                if self.tiles[x][y]["isMine"]:
                    self.placeMines(1, testing)
                else: 
                    self.tiles[x][y]["isMine"] = True
    
    # this method randoly places a random number of treasures in the game which is less than the number of mines
    # @Requires("numMines != None", "testing != None", "numMines >= 2", "typeOf(testing) == 'boolean'", "self.controller.tresureCoords != None")
    # @Ensures("self.treasures >= 0")
    # 
    # this method is in the model class because it a core element of the game     
    def placeTreasure(self, numMines, testing):
        if testing:
            for n in self.controller.tresureCoords:
                self.tiles[n["x"]][n["y"]]["isTreasure"] = True
                self.treasures += 1
        else:
            rangeNum = random.randint(1, numMines-1)
            for i in range(rangeNum):
                x = random.randint(0, self.controller.SIZE_X-1)
                y = random.randint(0, self.controller.SIZE_Y-1)
                if not self.tiles[x][y]["isMine"]:
                    self.tiles[x][y]["isTreasure"] = True
                    self.treasures += 1
    
    # this method checks if the game is over
    # 
    # this method is in the model class because it knows if the user won the game
    def gameOver(self, won):
        self.controller.checkMine()
        
        res = self.controller.view.askPlayAgain(won)

        if res:
            self.controller.restart()
        else:
            self.gameEnd = True
            self.controller.quit()
    
    # this method gets the neighbors of a tile
    # 
    # this method is in the model class because determines the neighbors of a tile is a core aspect of the game
    def getNeighbors(self, x, y):
        neighbors = []
        coords = [
            {"x": x-1,  "y": y-1},  #top right
            {"x": x-1,  "y": y},    #top middle
            {"x": x-1,  "y": y+1},  #top left
            {"x": x,    "y": y-1},  #left
            {"x": x,    "y": y+1},  #right
            {"x": x+1,  "y": y-1},  #bottom right
            {"x": x+1,  "y": y},    #bottom middle
            {"x": x+1,  "y": y+1},  #bottom left
        ]
        for n in coords:
            try:
                neighbors.append(self.tiles[n["x"]][n["y"]])
            except KeyError:
                pass
        return neighbors