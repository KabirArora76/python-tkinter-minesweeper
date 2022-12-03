from tkinter import *
from tkinter import messagebox as tkMessageBox
from collections import deque
import random
import platform
import time
from datetime import time, date, datetime

class View:
    
    def __init__(self, controller):
        self.controller = controller
        
        self.BTN_CLICK = "<Button-1>"
        self.BTN_FLAG = "<Button-2>" if platform.system() == 'Darwin' else "<Button-3>"
        
        self.startTime = None
        
        self.textUnicode = {
                "plain": '\u23F9',
                "clicked": ' ',
                "mine": '\u2299',
                "mineSafe": '\u29C6',
                "flag": '\u2691',
                "treasure": '\u2605',
                "wrong": "X"
            }
        
        if (not self.controller.textbased):
            # set up window
            self.tk = Tk()
            self.tk.title("Minesweeper")
        
            # import images
            self.images = {
                "plain": PhotoImage(file = "images/tile_plain.gif"),
                "clicked": PhotoImage(file = "images/tile_clicked.gif"),
                "mine": PhotoImage(file = "images/tile_mine.gif"),
                "mineSafe": PhotoImage(file = "images/tile_mineSafe.gif"),
                "flag": PhotoImage(file = "images/tile_flag.gif"),
                "wrong": PhotoImage(file = "images/tile_wrong.gif"),
                "treasure": PhotoImage(file = "images/tile_treasure.gif"),
                "numbers": []
            }
            for i in range(1, 9):
                self.images["numbers"].append(PhotoImage(file = "images/tile_"+str(i)+".gif"))

            # set up frame
            self.frame = Frame(self.tk)
            self.frame.pack()

            # set up labels/UI
            self.labels = {
                "time": Label(self.frame, text = "00:00:00"),
                "treasure": Label(self.frame, text = "Treasure: 0"),
                "mines": Label(self.frame, text = "Mines: 0"),
                "flags": Label(self.frame, text = "Flags: 0")
            }
            self.labels["time"].grid(row = 0, column = 0, columnspan = self.controller.SIZE_Y) # top full width
            self.labels["mines"].grid(row = self.controller.SIZE_X+1, column = 0, columnspan = int(self.controller.SIZE_Y/2)) # bottom left
            self.labels["flags"].grid(row = self.controller.SIZE_X+1, column = int(self.controller.SIZE_Y/2)-1, columnspan = int(self.controller.SIZE_Y/2)) # bottom right
            self.labels["treasure"].grid(row = self.controller.SIZE_X+2, column = 0, columnspan = self.controller.SIZE_Y) # bottom 1/3
    
    def restart(self):
        # start new game
        self.startTime = None
        if not self.controller.textbased:
            self.updateTimer()
        self.refreshLabels()
    
    # handles clicks on the UI
    # this method is in the view class becuase it is handling input from the user
    def onClickWrapper(self, x, y):
        return lambda Button: self.onClick(self.controller.model.tiles[int(x)][int(y)])
    
    # handles right clicks on the UI
    # this method is in the view class becuase it is handling input from the user
    def onRightClickWrapper(self, x, y):
        return lambda Button: self.onRightClick(self.controller.model.tiles[int(x)][int(y)])
    
    # handles events when tile is clicked
    # 
    # this method is moved to the view class because it is handling input from the user
    def onClick(self, tile):
        if tile["isMine"] == True and self.controller.model.treasureCredit <= 0:
            # end game
            self.controller.model.gameOver(False)
            return
        elif tile["isMine"] == True and self.controller.model.treasureCredit > 0:
            self.updateButton(tile, "mineSafe")
            self.controller.model.treasureCredit -= 1
            return
        
        if self.startTime == None:
            self.startTime = datetime.now()
        # change image
        if tile["mines"] == 0:
            self.updateButton(tile, "clicked")
            self.clearSurroundingTiles(tile["id"])
        elif tile["isTreasure"]:
            self.updateButton(tile, "treasure")
            self.controller.model.treasureCredit += 0.5
        else:
            self.updateButton(tile, "numbers", num=tile["mines"])
            
        # if not already set as clicked, change state and count
        if tile["state"] != self.controller.model.STATE_CLICKED:
            tile["state"] = self.controller.model.STATE_CLICKED
            self.controller.model.clickedCount += 1
        if self.controller.model.clickedCount == (self.controller.SIZE_X * self.controller.SIZE_Y) - self.controller.model.mines:
            self.controller.model.gameOver(True)
    
    # handles events when tile is right clicked
    # 
    # this method is moved to the view class because it is handling input from the user
    def onRightClick(self, tile):
        if self.startTime == None:
            self.startTime = datetime.now()

        # if not clicked
        if tile["state"] == self.controller.model.STATE_DEFAULT:
            self.updateButton(tile, "flag")
            tile["state"] = self.controller.model.STATE_FLAGGED
            if not self.controller.textbased:
                tile["button"].unbind(self.BTN_CLICK)
            # if a mine
            if tile["isMine"] == True:
                self.controller.model.correctFlagCount += 1
            self.controller.model.flagCount += 1
        # if flagged, unflag
        elif tile["state"] == 2:
            self.updateButton(tile, "plain")
            tile["state"] = 0
            if not self.controller.textbased:
                tile["button"].bind(self.BTN_CLICK, self.onClickWrapper(tile["coords"]["x"], tile["coords"]["y"]))
            # if a mine
            if tile["isMine"] == True:
                self.controller.model.correctFlagCount -= 1
            self.controller.model.flagCount -= 1
        self.refreshLabels()
    
    # clears the surrounds tiles that are not mines or treasures
    # 
    # this method is moved to the view class because it is controlling the view of the game
    def clearSurroundingTiles(self, id):
        queue = deque([id])

        while len(queue) != 0:
            key = queue.popleft()
            parts = key.split("_")
            x = int(parts[0])
            y = int(parts[1])

            for tile in self.controller.model.getNeighbors(x, y):
                self.clearTile(tile, queue)
    
    # clears the specific tile
    # 
    # this method is moved to the view class because it is controls an aspect of the view
    def clearTile(self, tile, queue):
        if tile["state"] != self.controller.model.STATE_DEFAULT:
            return

        if tile["mines"] == 0 and not tile["isTreasure"]:
            self.updateButton(tile, "clicked")
            queue.append(tile["id"])
        elif tile["isTreasure"]:
            self.updateButton(tile, "treasure")
            self.controller.model.treasureCredit += 0.5
        else:
            self.updateButton(tile, "numbers", num=tile["mines"])

        tile["state"] = self.controller.model.STATE_CLICKED
        self.controller.model.clickedCount += 1
    
    # refreshs the labels for the flags, mines and treasure count
    # 
    # this method is moved to the view class because it is control an aspect of the view
    def refreshLabels(self):
        if not self.controller.textbased:
            self.labels["flags"].config(text = "Flags: "+str(self.controller.model.flagCount))
            self.labels["mines"].config(text = "Mines: "+str(self.controller.model.mines))
            self.labels["treasure"].config(text = "Treasure: "+str(self.controller.model.treasures))
    
    # updates the timer for the UI
    # 
    # this method is moved to the view class because it is control an aspect of the view
    def updateTimer(self):
        ts = "00:00:00"
        if self.startTime != None:
            delta = datetime.now() - self.startTime
            ts = str(delta).split('.')[0] # drop ms
            if delta.total_seconds() < 36000:
                ts = "0" + ts # zero-pad
        self.labels["time"].config(text = ts)
        self.frame.after(100, self.updateTimer)
    
    # displays the board for the textbased view
    # 
    # this method is in the view class because it is control an aspect of the view
    def displayBoard(self):
        numString = '  '
        s = ''
        
        #Display x - range
        for i in range (0,self.controller.SIZE_Y):
            numString = numString + ' ' 
            if len(str(i)) == 1:
                numString = numString + '0'
            numString = numString + str(i)
        print (numString)
        
        #Display Board
        for x in range (0,self.controller.SIZE_X):
            s = str(x) if len(str(x)) != 1 else '0'+str(x)
            for y in range (0,self.controller.SIZE_Y):
                s  = s + '  ' + str(self.controller.model.tiles[int(x)][int(y)]['button'])
            print(s)    
        
        print("Flags: " + str(self.controller.model.flagCount) + " Mines: " + str(self.controller.model.mines) + " Treasure: " + str(self.controller.model.treasures))
    
    # gets the input from user 
    # 
    # this method is in the view class because it gets the input from the user
    def getNextMove(self):
        userIn = input("Flag or reveal square? (F - Flag, R - Reveal): ")
        y = input("Enter the column number: ")
        x = input("Enter the row number: ")
        # check the x and y inputs are numbers
        if (not x.isnumeric() or not y.isnumeric() or int(x) < 0 or int(y) < 0 or int(x) >= self.controller.SIZE_X or int(y) >= self.controller.SIZE_Y):
            return
        
        if userIn.lower() == 'r':
            self.onClick(self.controller.model.tiles[int(x)][int(y)])
        elif userIn.lower() == 'f':
            self.onRightClick(self.controller.model.tiles[int(x)][int(y)])
        return
    
    # asks the user if they want to play again
    # 
    # this method is in the view class because it is getting input from the user
    def askPlayAgain(self, won):
        if self.controller.textbased:
            self.displayBoard()
            msg = input("You Win! Play again? (Y, N): ") if won else input("You Lose! Play again? (Y, N): ")
            return True if msg.lower() == 'y' else False
        else:
            msg = "You Win! Play again?" if won else "You Lose! Play again?"
            return tkMessageBox.askyesno("Game Over", msg)
        
    # bings a button to the image of the UI
    # 
    # this method is moved to the view class because it controls the buttons on the UI which is a part of the view
    def bindButton(self, tile, x, y):
        tile["button"].bind(self.BTN_CLICK, self.onClickWrapper(x, y))
        tile["button"].bind(self.BTN_FLAG, self.onRightClickWrapper(x, y))
        tile["button"].grid( row = x+1, column = y ) # offset by 1 row for timer
    
    # makes a button object
    # 
    # this method is in the view class because it creates a button for the user to send input
    def makeButton(self, type, num = -1):
        return Button(self.frame, image = self.images[type]) if not self.controller.textbased else self.textUnicode[type]
    
    # updates the image of a button object
    # 
    # this methos is in the view class because it updates the image of a button
    def updateButton(self, tile, type, num = -1):
        if self.controller.textbased:
            if num == -1:
                tile["button"] = self.textUnicode[type]
            else:
                tile["button"] = num
        else: 
            tile["button"].config(image = self.images[type]) if num == -1 else tile["button"].config(image = self.images[type][num-1])