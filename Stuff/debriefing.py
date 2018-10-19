#! python3

from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from time import time, localtime, strftime, sleep

import random
import os.path
import os

from common import ExperimentFrame, InstructionsFrame, read_all, Measure
from gui import GUI




##################################################################################################################
# TEXTS #
#########

q1 = "V této poslední části nás zajímá, co si myslíte o průběhu experimentu. Napište v pár větách svůj názor."
q2 = "Máte nějaké připomínky k průběhu experimentu? Ke srozumitelnosti instrukcí, k přehlednosti uživatelského rozhraní, k chování experimentátorů, atp.? Co byste udělali jinak?"
q3 = "Co myslíte, že bylo cílem úkolů s předpověďmi, zda padne lichý či sudý počet bodů na kostce? Uveďte, proč jste se chovali v experimentu tak, jak jste se chovali."
q4 = "Co myslíte, že bylo cílem úkolu s možností darovat peníze charitě? Uveďte, proč jste se chovali v experimentu tak, jak jste se chovali."

##################################################################################################################



class Debriefing(ExperimentFrame):
    def __init__(self, root):
        super().__init__(root)

        self.file.write("Debriefing\n")

        self.question1 = Question(self, q1, alines = 6)
        self.question2 = Question(self, q2, alines = 6)
        self.question3 = Question(self, q3, alines = 6)
        self.question4 = Question(self, q4, alines = 6)

        self.question1.grid(row = 1, column = 1, sticky = "w")
        self.question2.grid(row = 2, column = 1, sticky = "w")
        self.question3.grid(row = 3, column = 1, sticky = "w")
        self.question4.grid(row = 4, column = 1, sticky = "w")
        
        ttk.Style().configure("TButton", font = "helvetica 15")
        self.next = ttk.Button(self, text = "Continue", command = self.nextFun)
        self.next.grid(row = 5, column = 1)

        self.warning = ttk.Label(self, text = "Please answer all questions.",
                                 background = "white", font = "helvetica 15", foreground = "white")
        self.warning.grid(row = 6, column = 1)

        self.columnconfigure(0, weight = 1)
        self.columnconfigure(2, weight = 1)
        self.rowconfigure(0, weight = 2)
        self.rowconfigure(1, weight = 1)
        self.rowconfigure(2, weight = 1)
        self.rowconfigure(3, weight = 1)
        self.rowconfigure(4, weight = 1)
        self.rowconfigure(5, weight = 1)
        self.rowconfigure(6, weight = 1)
        self.rowconfigure(7, weight = 2)

        
    def check(self):
        return self.question1.check() and self.question2.check() and \
               self.question3.check() and self.question4.check()

    def back(self):
        self.warning.config(foreground = "red")

    def write(self):
        self.file.write(self.id + "\t")
        self.question1.write(newline = False)
        self.file.write("\t")
        self.question2.write(newline = False)
        self.file.write("\t")
        self.question3.write(newline = False)
        self.file.write("\t")
        self.question4.write()


       
class Question(Canvas):
    def __init__(self, root, text, width = 80, qlines = 2, alines = 5):
        super().__init__(root)
        self["background"] = "white"
        self["highlightbackground"] = "white"
        self["highlightcolor"] = "white"

        self.root = root

        self.answer = StringVar()

        self.label = Text(self, width = width, wrap = "word", font = "helvetica 15",
                          relief = "flat", height = qlines, cursor = "arrow",
                          selectbackground = "white", selectforeground = "black")
        self.label.insert("1.0", text)
        self.label.config(state = "disabled")
        self.label.grid(column = 0, row = 0)

        self.field = Text(self, width = int(width*1.2), wrap = "word", font = "helvetica 13",
                          height = alines, relief = "solid")
        self.field.grid(column = 0, row = 1, pady = 10)

        self.columnconfigure(0, weight = 1)


    def check(self):
        return self.field.get("1.0", "end").strip()

    def write(self, newline = True):
        self.root.file.write(self.field.get("1.0", "end").replace("\n", "\t"))
        if newline:
            self.root.file.write("\n")

    def disable(self):
        self.field.config(state = "disabled")


            

def main():
    os.chdir(os.path.dirname(os.getcwd()))
    GUI([Debriefing])


if __name__ == "__main__":
    main()

