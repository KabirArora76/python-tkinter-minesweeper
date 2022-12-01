# from tkinter import *
# from tkinter import messagebox as tkMessageBox
from collections import deque
import random
import platform
import time
from datetime import time, date, datetime

class Model:
    def __init__(self, controller, multiple=False):
        
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
        self.mines = 0
        for x in range(0, self.controller.SIZE_X):
            for y in range(0, self.controller.SIZE_Y):
                if y == 0:
                    self.tiles[x] = {}

                id = str(x) + "_" + str(y)
                isMine = False

                # currently random amount of mines
                if random.uniform(0.0, 1.0) < 0.1:
                    isMine = True
                    self.mines += 1
                
                tile = {
                    "id": id,
                    "isMine": isMine,
                    "state": self.STATE_DEFAULT,
                    "coords": {
                        "x": x,
                        "y": y
                    },
                    "button": self.controller.makeButtonController("plain"),
                    "mines": 0 # calculated after grid is built
                }
                
                if multiple:
                    self.controller.updateButtonController(tile["button"], "plain")
                if not controller.textbased:
                    self.controller.bindButtonController(tile, x, y)

                self.tiles[x][y] = tile
                
        # loop again to find nearby mines and display number on tile
        for x in range(0, self.controller.SIZE_X):
            for y in range(0, self.controller.SIZE_Y):
                mc = 0
                for n in self.getNeighbors(x, y):
                    mc += 1 if n["isMine"] else 0
                self.tiles[x][y]["mines"] = mc
        
    def restart(self):
        # start new game
        self.controller.restart()
        
    def gameOver(self, won):
        self.controller.checkMine()
        
        res = self.controller.playAgain(won)

        if res:
            self.restart()
        else:
            self.gameEnd = True
            self.controller.quit()
    
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