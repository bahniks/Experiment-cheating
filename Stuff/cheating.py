#! python3
from tkinter import *
from tkinter import ttk
from time import perf_counter, sleep

import random
import os

from common import ExperimentFrame, InstructionsFrame
from gui import GUI


################################################################################
# TEXTS
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
wintext = "vyhráli 50,- Kč."
losstext = "nevyhráli nic."

choicetext = """Jak jste si všimli, tento experimentální úkol nabýval dvou podob:

Zaznamenali jste, jakou stranu předpovídáte. Poté proběhl hod a následně jste se dozvěděli, zda jste vyhráli či nikoliv.
Rozhodli jste se, jakou stranu předpovídáte. Poté proběhl hod a následně jste sami určili, zda jste vyhráli či nikoliv.

Nyní proběhne posledních 10 kol úkolu. Můžete si sami vybrat, zda je chcete řešit v podobě 1. nebo v podobě 2.
"""

continuetext = "Pokračovat"
oddtext = "Liché"
eventext = "Sudé"
rolltext = "Hodit kostkou"
correcttext = "Uhodl(a)"
incorrecttext = "Neuhodl(a)"
           

intro_block_1 = """
Intro1
"""

intro_block_2 = """
Intro2
"""

intro_block_3 = """
Intro3
"""
################################################################################


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
        self.pause_after_roll = 0.5
        self.pause_before_trial = 0.2
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
        self.rowconfigure(0, weight = 3)
        self.rowconfigure(1, weight = 1)
        self.rowconfigure(2, weight = 1)
        self.rowconfigure(3, weight = 1)
        self.rowconfigure(4, weight = 1)
        self.rowconfigure(5, weight = 1)
        self.rowconfigure(6, weight = 4)

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
            self.rollButton = ttk.Button(self.upperButtonFrame, text = rolltext,
                                         command = self.roll)
            self.rollButton.grid(row = 0, column = 1)
        elif self.condition == "control":
            self.upperText.insert("1.0", controltext.format(self.currentTrial))
            self.evenButton = ttk.Button(self.upperButtonFrame, text = eventext,
                                         command = lambda: self.roll("even"))
            self.oddButton = ttk.Button(self.upperButtonFrame, text = oddtext,
                                        command = lambda: self.roll("odd"))
            self.evenButton.grid(row = 0, column = 0, padx = 30)
            self.oddButton.grid(row = 0, column = 2, padx = 30)
        self.upperText["state"] = "disabled"


    def bottomPart(self):
        self.bottomText["state"] = "normal"
        if self.condition == "treatment":
            self.bottomText.insert("1.0", treatmenttext2)
            self.winButton = ttk.Button(self.bottomButtonFrame, text = correcttext,
                                         command = lambda: self.answer("win"))
            self.lossButton = ttk.Button(self.bottomButtonFrame, text = incorrecttext,
                                        command = lambda: self.answer("loss"))
            self.winButton.grid(row = 0, column = 0, padx = 30)
            self.lossButton.grid(row = 0, column = 2, padx = 30)
        elif self.condition == "control":
            text = wintext if (self.response == "odd" and self.currentRoll in (1,3,5)) or (
                self.response == "even" and self.currentRoll in (2,4,6)) else losstext
            self.bottomText.insert("1.0", controltext2.format(text))
            self.continueButton = ttk.Button(self.bottomButtonFrame, text = continuetext,
                                             command = self.answer)
            self.continueButton.grid(row = 0, column = 1)
        self.bottomText["state"] = "disabled"


    def roll(self, response = "NA"):
        self.firstResponse = perf_counter()
        if self.condition == "treatment":
            self.rollButton["state"] = "disabled"
        else:
            self.evenButton["state"] = "disabled"
            self.oddButton["state"] = "disabled"
        self.currentRoll = random.randint(1, 6)
        self.die.create_rectangle((5, 5, self.diesize - 5, self.diesize - 5),
                                  fill = "white", tag = "die", outline = "black", width = 5)
        self.displayNum(self.diesize/2, self.diesize/2, self.currentRoll)
        self.response = response
        self.update()
        sleep(self.pause_after_roll)
        self.beforeSecondResponse = perf_counter()
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


    def answer(self, answer = "NA"):
        t = perf_counter()
        self.responses.append([self.currentTrial, self.condition, self.currentRoll, self.response,
                               answer, t - self.time, self.firstResponse - self.time,
                               t - self.beforeSecondResponse])
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
        sleep(self.pause_before_trial)
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

