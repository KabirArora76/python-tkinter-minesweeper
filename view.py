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
                "mine": '\u22A1',
                "flag": '\u2691',
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
                "flag": PhotoImage(file = "images/tile_flag.gif"),
                "wrong": PhotoImage(file = "images/tile_wrong.gif"),
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
                "mines": Label(self.frame, text = "Mines: 0"),
                "flags": Label(self.frame, text = "Flags: 0")
            }
            self.labels["time"].grid(row = 0, column = 0, columnspan = self.controller.SIZE_Y) # top full width
            self.labels["mines"].grid(row = self.controller.SIZE_X+1, column = 0, columnspan = int(self.controller.SIZE_Y/2)) # bottom left
            self.labels["flags"].grid(row = self.controller.SIZE_X+1, column = int(self.controller.SIZE_Y/2)-1, columnspan = int(self.controller.SIZE_Y/2)) # bottom right
    
    def restart(self):
        # start new game
        self.startTime = None
        if not self.controller.textbased:
            self.updateTimer()
        self.refreshLabels()
    
    def refreshLabels(self):
        if not self.controller.textbased:
            self.labels["flags"].config(text = "Flags: "+str(self.controller.getFlagCount()))
            self.labels["mines"].config(text = "Mines: "+str(self.controller.getMines()))
    
    def updateTimer(self):
        ts = "00:00:00"
        if self.startTime != None:
            delta = datetime.now() - self.startTime
            ts = str(delta).split('.')[0] # drop ms
            if delta.total_seconds() < 36000:
                ts = "0" + ts # zero-pad
        self.labels["time"].config(text = ts)
        self.frame.after(100, self.updateTimer)
        
    def displayBoard(self):
        numString = ' '
        s = ''
        
        #Display x - range
        for i in range (0,self.controller.SIZE_Y):
            numString = numString + ' ' + str(i)
        print (numString)
        
        #Display Board
        for r in range (0,self.controller.SIZE_X):
            s = str (r)
            for c in range (0,self.controller.SIZE_Y):
                s  = s + ' ' + str(self.controller.getTile(r,c)['button'])
            print(s)    
        
        print("Flags: " + str(self.controller.getFlagCount()) + " Mines: " + str(self.controller.getMines()))
    
    def getNextMove(self):
        userIn = input("Flag or reveal square? (F - Flag, R - Reveal): ")
        y = input("Enter the column number: ")
        x = input("Enter the row number: ")
        # check the x and y inputs are numbers
        if (not x.isnumeric() or not y.isnumeric() or int(x) < 0 or int(y) < 0 or int(x) >= self.controller.SIZE_X or int(y) >= self.controller.SIZE_Y):
            return
        
        if userIn.lower() == 'r':
            self.controller.onClick(self.controller.getTile(int(x), int(y)))
        elif userIn.lower() == 'f':
            self.controller.onRightClick(self.controller.getTile(int(x), int(y)))
        return
    
    def askPlayAgain(self, won):
        if self.controller.textbased:
            self.displayBoard()
            msg = input("You Win! Play again? (Y, N): ") if won else input("You Lose! Play again? (Y, N): ")
            return True if msg.lower() == 'y' else False
        else:
            msg = "You Win! Play again?" if won else "You Lose! Play again?"
            return tkMessageBox.askyesno("Game Over", msg)
        
    def bindButton(self, tile, x, y):
        tile["button"].bind(self.BTN_CLICK, self.controller.onClickWrapper(x, y))
        tile["button"].bind(self.BTN_FLAG, self.controller.onRightClickWrapper(x, y))
        tile["button"].grid( row = x+1, column = y ) # offset by 1 row for timer
    
    def makeButton(self, type, num = -1):
        return Button(self.frame, image = self.images[type]) if not self.controller.textbased else self.textUnicode[type]
            
    def updateButton(self, tile, type, num = -1):
        if self.controller.textbased:
            if num == -1:
                tile["button"] = self.textUnicode[type]
            else:
                tile["button"] = num
        else: 
            tile["button"].config(image = self.images[type]) if num == -1 else tile["button"].config(image = self.images[type][num-1])