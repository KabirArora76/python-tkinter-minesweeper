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
    # Initialize the controller object
    # @param textbased - if the game is textbased
    # @param diff - the difficulty of the game 
    def __init__(self, textbased, diff):    
        
        # set the difficulty of the game and update the number of mines
        self.numMines = 0
        self.setDiff(diff)
        
        self.textbased = textbased
        
        # initialize the view and model
        self.view = View(self)
        self.model = Model(self, self.numMines)
        
        # init the timer for non textbased game
        if not self.textbased:
            self.view.updateTimer() # init timer
     
        self.view.refreshLabels()
    
    # sets the difficutly for the game
    # @Requires 
    # @Ensures
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
        self.model = Model(self, self.numMines)
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