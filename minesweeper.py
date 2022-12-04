# Python Version 2.7.3
# File: minesweeper.py

from tkinter import *
from tkinter import messagebox as tkMessageBox
from collections import deque
import random
import platform
import time
from datetime import time, date, datetime
from controller import Controller
# imports for running in VS code ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ REMOVE BEFORE SUBMISSION
import os 
import sys

# if statement is only so that I can run this in VS code ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ REMOVE BEFORE SUBMISSION
if sys.argv:
    filepath = sys.argv[0]
    folder, filename = os.path.split(filepath)
    os.chdir(folder) # now your working dir is the parent folder of the script

def main():
    textbased = False
    difficulty = ["beginner", "intermediate", "expert"]
    # create game instance
    controller = Controller(textbased, difficulty[0])
    
    controller.startGame()

if __name__ == "__main__":
    main()
