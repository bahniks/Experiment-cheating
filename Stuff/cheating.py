#! python3
from tkinter import *
from tkinter import ttk
from time import perf_counter, sleep

import random
import os

from common import ExperimentFrame, InstructionsFrame
from gui import GUI


treatmenttext = '''{}. kolo

Rozhodněte se, zda v tomto kole na kostce padne lichý či sudý počet bodů.

Svoji volbu si zapamatujte.

Zmáčkněte tlačítko "Hodit kostkou".
'''

treatmenttext2 = "Stanovte, zda jste uhodli a vyhráli 50,- Kč nebo neuhodli a nevyhráli nic."

controltext = """{}. kolo

Rozhodněte se, zda v tomto kole na kostce padne lichý či sudý počet bodů.
"""

controltext2 = "V tomto kole jste {}"
win = "vyhráli 50,- Kč."
loss = "nevyhráli nic."


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
        self.displayNum = self.createDots # self.createDots or self.createText
        self.diesize = 240
        #######################

        self.condition = condition

        self.width = self.root.screenwidth
        self.height = self.root.screenheight

        self.file.write("Cheating {}\n".format(block))

        self.upperText = Text(self, height = 8, width = 80, relief = "flat", font = "helvetica 15")
        self.upperButtonFrame = Canvas(self, highlightbackground = "white", highlightcolor = "white",
                                       background = "white", height = 100)
        self.die = Canvas(self, highlightbackground = "white", highlightcolor = "white",
                          background = "white", width = self.diesize, height = self.diesize)
        self.bottomText = Text(self, height = 3, width = 80, relief = "flat", font = "helvetica 15")
        self.bottomButtonFrame = Canvas(self, highlightbackground = "white", highlightcolor = "white",
                                        background = "white", height = 100)

        self.upperText.grid(column = 1, row = 1)
        self.upperButtonFrame.grid(column = 1, row = 2)
        self.die.grid(column = 1, row = 3, pady = 40)
        self.bottomText.grid(column = 1, row = 4)
        self.bottomButtonFrame.grid(column = 1, row = 5)
        self._createFiller()

        self["highlightbackground"] = "white"
        self.columnconfigure(1, weight = 1)
        self.rowconfigure(0, weight = 2)
        self.rowconfigure(1, weight = 1)
        self.rowconfigure(2, weight = 1)
        self.rowconfigure(3, weight = 2)
        self.rowconfigure(4, weight = 1)
        self.rowconfigure(5, weight = 1)
        self.rowconfigure(6, weight = 1)

        self.currentTrial = 0

        ttk.Style().configure("TButton", font = "helvetica 15")

        self.responses = []


    def run(self):
        self.bottomText["state"] = "disabled"
        self.upperText["state"] = "disabled"
        if self.currentTrial < self.trials:
            self.currentTrial += 1
            self.startTrial()
        else:
            self.nextFun()


    def startTrial(self):
        self.time = perf_counter()
        self.upperPart()


    def _createFiller(self):
        self.fillerFrame = Canvas(self.bottomButtonFrame, highlightbackground = "white",
                                  highlightcolor = "white", background = "white", height = 100, width = 1)
        self.fillerFrame.grid(column = 0, row = 0, sticky = NS)


    def upperPart(self):
        self.upperText["state"] = "normal"
        if self.condition == "treatment":
            self.upperText.insert("1.0", treatmenttext.format(self.currentTrial))
            self.rollButton = ttk.Button(self.upperButtonFrame, text = "Hodit kostkou",
                                         command = self.roll)
            self.rollButton.grid(row = 0, column = 1)
        elif self.condition == "control":
            self.upperText.insert("1.0", controltext.format(self.currentTrial))
            self.evenButton = ttk.Button(self.upperButtonFrame, text = "Sudé",
                                         command = lambda: self.roll("even"))
            self.oddButton = ttk.Button(self.upperButtonFrame, text = "Liché",
                                        command = lambda: self.roll("odd"))
            self.evenButton.grid(row = 0, column = 0, padx = 30)
            self.oddButton.grid(row = 0, column = 2, padx = 30)
        self.upperText["state"] = "disabled"


    def bottomPart(self):
        self.bottomText["state"] = "normal"
        if self.condition == "treatment":
            self.bottomText.insert("1.0", treatmenttext2)
            self.winButton = ttk.Button(self.bottomButtonFrame, text = "Uhodl(a)",
                                         command = lambda: self.answer("win"))
            self.lossButton = ttk.Button(self.bottomButtonFrame, text = "Neuhodl(a)",
                                        command = lambda: self.answer("loss"))
            self.winButton.grid(row = 0, column = 0, padx = 30)
            self.lossButton.grid(row = 0, column = 2, padx = 30)
        elif self.condition == "control":
            text = win if self.response == "odd" and self.currentRoll in (1,3,5) else loss
            self.bottomText.insert("1.0", controltext2.format(text))
            self.continueButton = ttk.Button(self.bottomButtonFrame, text = "Pokračovat",
                                             command = self.answer)
            self.continueButton.grid(row = 0, column = 1)
        self.bottomText["state"] = "disabled"
            

    def roll(self, response = None):
        if self.condition == "treatment":
            self.rollButton["state"] = "disabled"
        else:
            self.evenButton["state"] = "disabled"
            self.oddButton["state"] = "disabled"
        self.currentRoll = random.randint(1, 6)
        self.die.create_rectangle((2, 2, self.diesize - 2, self.diesize - 2),
                                  fill = "white", tag = "die", outline = "black", width = 5)
        self.displayNum(self.diesize/2, self.diesize/2, self.currentRoll)
        self.response = response
        self.bottomPart()


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


    def answer(self, answer = None):
        #self.responses.append([self.currentTrial, self.phase, response, self.angle, self.angleDist,
        #                       correct, t - self.time] + self.diceAngles + self.numbers +
        #                      self.colors + [self.root.charity, self.root.reward, forCharity])
        self.bottomText["state"] = "normal"
        self.upperText["state"] = "normal"
        self.die.delete("die")
        self.upperText.delete("1.0", "end")
        self.bottomText.delete("1.0", "end")
        for child in self.upperButtonFrame.winfo_children():
            child.grid_remove()
        for child in self.bottomButtonFrame.winfo_children():
            child.grid_remove()
        self._createFiller()
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

