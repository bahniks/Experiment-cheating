#! python3
from tkinter import *
from tkinter import ttk

import os
import random

from collections import OrderedDict

from common import ExperimentFrame
from gui import GUI
from constants import CURRENCY, WIN, COUNTRY


################################################################################
# TEXTS

optionsChina = ((50, 60, 70, 80, 90),
                ("30%", "40%", "50%", "60%", "70%"),
                (100, 100, 100, 100, 100))
optionsCzechia = ((50, 60, 70, 80, 90),
                  ("30%", "40%", "50%", "60%", "70%"),
                  (100, 100, 100, 100, 100))

instructions = """
vyberte si loterie, co preferujete

loterie znamenaji

toto je placeholder text

a toto take
"""



################################################################################


class Lottery(ExperimentFrame):
    def __init__(self, root):
        super().__init__(root)
           


        self.text = Text(self, font = "helvetica 15", relief = "flat", background = "white", height = 10,
                         wrap = "word", highlightbackground = "white", width = 90)
        self.text.grid(row = 1, column = 0, columnspan = 4)
        self.text.insert("1.0", instructions)
        self.text.config(state = "disabled")

        if COUNTRY == "CHINA":
            options = optionsChina
        elif COUNTRY == "CZECHIA":
            options = optionsCzechia

        self.variables = OrderedDict()
        self.rbuttonsL = {}
        self.rbuttonsR = {}
        for i in range(5):
            row = i + 3
            self.variables[i] = StringVar()
            self.rbuttonsL[i] = ttk.Radiobutton(self, text = " {} {}".format(options[0][i], CURRENCY),
                                                variable = self.variables[i], value = str(i+1) + "sure",
                                                command = self.checkAllFilled)
            self.rbuttonsL[i].grid(column = 1, row = row, sticky = W, padx = 30)
            self.rbuttonsR[i] = ttk.Radiobutton(self, variable = self.variables[i], value = str(i+1) + "risky",
                                                text = " {} {} {}".format(options[1][i], options[2][i], CURRENCY),
                                                command = self.checkAllFilled)
            self.rbuttonsR[i].grid(column = 2, row = row, sticky = W, padx = 30)

        ttk.Style().configure("TRadiobutton", background = "white", font = "helvetica 15")
        ttk.Style().configure("TButton", font = "helvetica 15")

        self.columnconfigure(0, weight = 1)
        self.columnconfigure(3, weight = 1)
        self.rowconfigure(0, weight = 1)
        self.rowconfigure(1, weight = 1)
        self.rowconfigure(9, weight = 1)
        self.rowconfigure(10, weight = 1)

        self.next = ttk.Button(self, text = "Continue", command = self.nextFun)
        self.next.grid(row = 9, column = 0, columnspan = 4, pady = 15)
        self.next["state"] = "disabled"
        

    def checkAllFilled(self):
        if all([var.get() for var in self.variables.values()]):
            self.next["state"] = "!disabled"


    def write(self):
        self.file.write("Charity\n")
        self.file.write("\t".join([self.id] + [var.get() for var in self.variables.values()]) + "\n")


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.getcwd()))
    GUI([Lottery])
