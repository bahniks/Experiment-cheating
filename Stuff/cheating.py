#! python3
from tkinter import *
from tkinter import ttk
from time import perf_counter, sleep

import random
import os

from common import ExperimentFrame, InstructionsFrame
from gui import GUI


intro_block_1 = """
Intro1
"""

intro_block_2 = """
Intro2
"""

intro_block_3 = """
Intro3
"""

conditions = ["treatment", "control"]
random.shuffle(conditions)
if random.random() < 0.5:
    if random.random() < 0.5:
        conditions.append("treatment")
    else:
        conditions.append("control")
else:
    conditions.append("choice")

Instructions1 = (InstructionsFrame, {"text": intro_block_1, "height": 5})
Instructions2 = (InstructionsFrame, {"text": intro_block_2, "height": 5})
Instructions3 = (InstructionsFrame, {"text": intro_block_3, "height": 5})


class Cheating(ExperimentFrame):
    def __init__(self, root, condition, block):
        super().__init__(root)

        #######################
        # adjustable parameters
        self.trials = 10
        self.pause = 1
        self.numRange = (1,6)
        self.displayNum = self.createDots # self.createDots or self.createText
        self.diesize = 300
        #######################

        self.condition = condition

        self.width = self.root.screenwidth
        self.height = self.root.screenheight

        self.file.write("Cheating {}\n".format(block))

        self.upperText = Text(self, height = 3, width = 80, relief = "flat", font = "helvetica 12")
        self.upperButtonFrame = Canvas(self, highlightbackground = "white", highlightcolor = "white",
                                       background = "white", height = 100)
        self.die = Canvas(self, highlightbackground = "white", highlightcolor = "white",
                          background = "white", width = self.diesize, height = self.diesize)
        self.bottomText = Text(self, height = 3, width = 80, relief = "flat", font = "helvetica 12")
        self.bottomButtonFrame = Canvas(self, highlightbackground = "white", highlightcolor = "white",
                                        background = "white", height = 100)

        self.upperText.grid(column = 1, row = 1)
        self.upperButtonFrame.grid(column = 1, row = 2)
        self.die.grid(column = 1, row = 3)
        self.bottomText.grid(column = 1, row = 4)
        self.bottomButtonFrame.grid(column = 1, row = 5)

        self["highlightbackground"] = "white"
        self.columnconfigure(1, weight = 1)
        self.rowconfigure(0, weight = 1)
        self.rowconfigure(6, weight = 1)

        self.currentTrial = 0

        ttk.Style().configure("TButton", font = "helvetica 15")

        #if not hasattr(self.root, "charity"):
        #    self.root.charity = 0
        #    self.root.reward = 0

        self.responses = []


    def run(self):        
        if self.currentTrial < self.trials:
            self.currentTrial += 1
            self.startTrial()
        else:
            self.nextFun()


    def startTrial(self):
        self.time = perf_counter()
        self.upperPart()


    def upperPart(self):
        if self.condition == "treatment":
            self.upperText.insert("1.0", "treatment text")
            self.rollButton = ttk.Button(self.upperButtonFrame, text = "Hodit kostkou",
                                         command = self.roll)
            self.rollButton.grid(row = 0, column = 1)
        elif self.condition == "control":
            self.upperText.insert("1.0", "control text")
            self.evenButton = ttk.Button(self.upperButtonFrame, text = "Sudé",
                                         command = lambda: self.roll("even"))
            self.oddButton = ttk.Button(self.upperButtonFrame, text = "Liché",
                                        command = lambda: self.roll("odd"))
            self.evenButton.grid(row = 0, column = 0)
            self.oddButton.grid(row = 0, column = 2)
            

    def roll(self, response = None):
        dots = random.randint(1, 6)
        self.die.create_rectangle((2, 2, self.diesize - 2, self.diesize - 2),
                                  fill = "white", tag = "die", outline = "black", width = 4)
        self.displayNum(self.diesize/2, self.diesize/2, dots)


    def createDots(self, x0, y0, num):
        positions = {"1": [(0,0)],
                     "2": [(-1,-1), (1,1)],
                     "3": [(-1,-1), (0,0), (1,1)],
                     "4": [(-1,-1), (-1,1), (1,-1), (1,1)],
                     "5": [(-1,-1), (-1,1), (0,0), (1,-1), (1,1)],
                     "6": [(-1,-1), (-1,1), (1,-1), (1,1), (-1,0), (1,0)]}
        for x, y in positions[str(num)]:
            d = self.diesize/4
            coords = [x0 + x*d + d/3, y0 - y*d + d/3,
                      x0 + x*d - d/3, y0 - y*d - d/3]
            self.die.create_oval(tuple(coords), fill = "black", tag = "die")


    def createText(self, x0, y0, num):
        self.die.create_text(x0, y0, text = str(num), font = "helvetica 70", tag = "die")


    def response(self, e):
        self.responses.append([self.currentTrial, self.phase, response, self.angle, self.angleDist,
                               correct, t - self.time] + self.diceAngles + self.numbers +
                              self.colors + [self.root.charity, self.root.reward, forCharity])
        self.delete("die")
        self.update()
        self.run()
        
                   
    def write(self):
        for response in self.responses:
            begin = [self.id]
            self.file.write("\t".join(map(str, begin + response)) + "\n")




BlockOne = (Cheating, {"condition": conditions[0], "block": 1})
BlockTwo = (Cheating, {"condition": conditions[1], "block": 2})
BlockThree = (Cheating, {"condition": conditions[2], "block": 3})


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.getcwd()))
    GUI([#Instructions1,
         BlockOne,
         Instructions2,
         BlockTwo,
         Instructions3,
         BlockThree
         ])

