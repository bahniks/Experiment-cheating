#! python3
from tkinter import *
from tkinter import ttk

import os

from common import ExperimentFrame, InstructionsFrame
from gui import GUI



questintro = """
V následující části bude uvedena řada výroků.

Přečtěte si, prosím, postupně každý výrok a vždy se rozhodněte, jak moc s ním souhlasíte nebo nesouhlasíte.
"""

QuestInstructions = (InstructionsFrame, {"text": questintro, "height": 5})



hexacoinstructions = """On the following pages you will find a series of statements about you.
Please read each statement and decide how much you agree or disagree with that statement.
"""

agencyinstructions = "Please indicate the extent to which you agree with the following statements."

bidrinstructions = "Please read each statement and indicate how true it is."

workinstructions = "How comfortable would feel about engaging in the following behaviors at work?"



class Quest(ExperimentFrame):
    def __init__(self, root, perpage, file, name, left, right, options = 5,
                 instructions = "", height = 3, width = 80, center = False):
        super().__init__(root)

        self.perpage = perpage
        self.left = left
        self.right = right
        self.options = options

        self.file.write("{}\n".format(name))

        if instructions:
            self.instructions = Text(self, height = height, relief = "flat", width = width,
                                     font = "helvetica 16", wrap = "word")
            self.instructions.grid(row = 1, column = 0, columnspan = 3)
            self.instructions.insert("1.0", instructions, "text")
            if center:
                self.instructions.tag_config("text", justify = "center") 
            self.instructions["state"] = "disabled"

        self.questions = []
        with open(os.path.join("Stuff", file)) as f:
            for line in f:
                self.questions.append(line.strip())

        ttk.Style().configure("TButton", font = "helvetica 15")
        self.next = ttk.Button(self, text = "Continue", command = self.nextFun,
                               state = "disabled")
        self.next.grid(row = self.perpage*2 + 4, column = 1)

        self.rowconfigure(0, weight = 1)
        self.rowconfigure(1, weight = 2)
        self.rowconfigure(self.perpage*2 + 4, weight = 1)
        self.rowconfigure(self.perpage*2 + 5, weight = 3)
        self.columnconfigure(0, weight = 1)
        self.columnconfigure(2, weight = 1)

        self.mnumber = 0
        
        self.createQuestions()


    def createQuestions(self):
        self.measures = []
        for i in range(self.perpage):
            m = Likert(self, self.questions[self.mnumber], shortText = str(self.mnumber + 1),
                       left = self.left, right = self.right, options = self.options)
            m.grid(column = 0, columnspan = 3, row = i*2 + 3)
            self.rowconfigure(i*2 + 4, weight = 1)
            self.mnumber += 1
            self.measures.append(m)
            if self.mnumber == len(self.questions):
                break


    def nextFun(self):
        for measure in self.measures:
            measure.write()
            measure.grid_forget()
        if self.mnumber == len(self.questions):
            self.file.write("\n")
            self.destroy()
            self.root.nextFrame()
        else:
            self.next["state"] = "disabled"
            self.createQuestions()


    def check(self):
        for m in self.measures:
            if not m.answer.get():
                return
        else:
            self.next["state"] = "!disabled"



class Likert(Canvas):
    def __init__(self, root, text, shortText = "", options = 5,
                 left = "strongly disagree", right = "strongly agree"):
        super().__init__(root)

        self.root = root
        self.text = shortText
        self.answer = StringVar()
        self["background"] = "white"
        self["highlightbackground"] = "white"
        self["highlightcolor"] = "white"

        ttk.Style().configure("TRadiobutton", background = "white", font = "helvetica 13")

        self.question = ttk.Label(self, text = text, background = "white",
                                  anchor = "center", font = "helvetica 14")
        self.question.grid(column = 0, row = 0, columnspan = options + 2, sticky = S)

        self.left = ttk.Label(self, text = left, background = "white",
                              font = "helvetica 13")
        self.right = ttk.Label(self, text = right, background = "white",
                               font = "helvetica 13")
        self.left.grid(column = 0, row = 1, sticky = E, padx = 5)
        self.right.grid(column = options + 1, row = 1, sticky = W, padx = 5)           

        for value in range(1, options + 1):
            ttk.Radiobutton(self, text = str(value), value = value, variable = self.answer,
                            command = self.check).grid(row = 1, column = value, padx = 4)

        self.columnconfigure(0, weight = 1)
        self.columnconfigure(options + 1, weight = 1)
        self.rowconfigure(0, weight = 1)


    def write(self):
        ans = "{}\t{}\n".format(self.text, self.answer.get())
        self.root.file.write(self.root.id + "\t" + ans)


    def check(self):
        self.root.check()





class Hexaco(Quest):
    def __init__(self, root):
        super().__init__(root, 10, "hexaco.txt", "Hexaco", instructions = hexacoinstructions, width = 80,
                         left = "strongly disagree", right = "strongly agree",
                         height = 2, options = 5, center = True)

class BIDR(Quest):
    def __init__(self, root):
        super().__init__(root, 8, "BIDR.txt", "BIDR", instructions = bidrinstructions, center = True,
                         left = "not true", right = "very true", height = 1, options = 7)

class Agency(Quest):
    def __init__(self, root):
        super().__init__(root, 7, "agency.txt", "Moral agency", instructions = agencyinstructions, center = True,
                         left = "strongly disagree", right = "strongly agree", height = 1, options = 5)
        
class Disengagement(Quest):
    def __init__(self, root):
        super().__init__(root, 6, "disengagement.txt", "Moral disengagement", instructions = agencyinstructions,
                         left = "strongly disagree", right = "strongly agree",
                         height = 1, options = 7, center = True)

class Work(Quest):
    def __init__(self, root):
        super().__init__(root, 7, "work.txt", "Work deception", instructions = workinstructions,
                         left = "very uncomfortable", right = "very comfortable",
                         height = 1, options = 7, center = True)





if __name__ == "__main__":
    os.chdir(os.path.dirname(os.getcwd()))
    GUI([QuestInstructions,
         Hexaco,
         Work,
         BIDR,
         Agency,
         Disengagement])
