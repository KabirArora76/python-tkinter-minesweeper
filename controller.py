from tkinter import *
from tkinter import messagebox as tkMessageBox
from collections import deque
import random
import platform
import time
from datetime import time, date, datetime
from model import Model
from view import View

class Controller:
    def __init__(self, textbased):    
        
        self.SIZE_X = 10
        self.SIZE_Y = 10
        
        self.textbased = textbased
        self.view = View(self)
        self.model = Model(self)
        
        if 'self.view' in locals() and self.textbased:
            self.view = View(self.textbased)
        if not self.textbased:
            self.view.updateTimer() # init timer
            
        self.view.refreshLabels()
    
    def restart(self):
        self.model = Model(self)
        self.view.restart()
        
    
    def onClickWrapper(self, x, y):
        return lambda Button: self.onClick(self.model.tiles[x][y])
    
    def onRightClickWrapper(self, x, y):
        return lambda Button: self.onRightClick(self.model.tiles[x][y])
    
    def onClick(self, tile):
        if tile["isMine"] == True:
            # end game
            self.model.gameOver(False)
            return
        
        if self.view.startTime == None:
            self.view.startTime = datetime.now()
        # change image
        if tile["mines"] == 0:
            self.view.updateButton(tile, "clicked")
            self.clearSurroundingTiles(tile["id"])
        else:
            self.view.updateButton(tile, "numbers", num=tile["mines"])
            
        # if not already set as clicked, change state and count
        if tile["state"] != self.model.STATE_CLICKED:
            tile["state"] = self.model.STATE_CLICKED
            self.model.clickedCount += 1
        if self.model.clickedCount == (self.SIZE_X * self.SIZE_Y) - self.model.mines:
            self.model.gameOver(True)
    
    def onRightClick(self, tile):
        if self.view.startTime == None:
            self.view.startTime = datetime.now()

        # if not clicked
        if tile["state"] == self.model.STATE_DEFAULT:
            self.view.updateButton(tile, "flag")
            tile["state"] = self.model.STATE_FLAGGED
            if not self.textbased:
                tile["button"].unbind(self.view.BTN_CLICK)
            # if a mine
            if tile["isMine"] == True:
                self.model.correctFlagCount += 1
            self.model.flagCount += 1
        # if flagged, unflag
        elif tile["state"] == 2:
            self.view.updateButton(tile, "plain")
            tile["state"] = 0
            if not self.textbased:
                tile["button"].bind(self.view.BTN_CLICK, self.onClickWrapper(tile["coords"]["x"], tile["coords"]["y"]))
            # if a mine
            if tile["isMine"] == True:
                self.model.correctFlagCount -= 1
            self.model.flagCount -= 1
        self.view.refreshLabels()
                
    def clearSurroundingTiles(self, id):
        queue = deque([id])

        while len(queue) != 0:
            key = queue.popleft()
            parts = key.split("_")
            x = int(parts[0])
            y = int(parts[1])

            for tile in self.model.getNeighbors(x, y):
                self.clearTile(tile, queue)
                
    def clearTile(self, tile, queue):
        if tile["state"] != self.model.STATE_DEFAULT:
            return

        if tile["mines"] == 0:
            self.view.updateButton(tile, "clicked")
            queue.append(tile["id"])
        else:
            self.view.updateButton(tile, "numbers", num=tile["mines"])

        tile["state"] = self.model.STATE_CLICKED
        self.model.clickedCount += 1

    def startGame(self):
        if self.textbased:
            while (not self.model.gameEnd):
                self.view.displayBoard()
                self.view.getNextMove()
        else:
            self.view.tk.mainloop()
            
    def checkMine(self):
        for x in range(0, self.SIZE_X):
            for y in range(0, self.SIZE_Y):
                if self.model.tiles[x][y]["isMine"] == False and self.model.tiles[x][y]["state"] == self.model.STATE_FLAGGED:
                    self.view.updateButton(self.model.tiles[x][y], "wrong")
                if self.model.tiles[x][y]["isMine"] == True and self.model.tiles[x][y]["state"] != self.model.STATE_FLAGGED:
                    self.view.updateButton(self.model.tiles[x][y], "mine")
        if not self.textbased:
            self.view.tk.update()
        
    def playAgain(self, won):
        return self.view.askPlayAgain(won)
    
    def quit(self):
        if not self.textbased:
            self.view.tk.quit()
            
    def getFlagCount(self):
        return self.model.flagCount
    
    def getTile(self, x, y):
        return self.model.tiles[x][y]
    
    def getMines(self):
        return self.model.mines
    
    def bindButtonController(self, tile, x, y):
        return self.view.bindButton(tile, x, y)
        
    def makeButtonController(self, type):
        return self.view.makeButton(type)
    
    def updateButtonController(self, button, type):
        return self.view.updateButton(button, type)