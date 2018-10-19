#! python3
from tkinter import *
from tkinter import ttk
from time import perf_counter, sleep

import random
import os

from common import ExperimentFrame, InstructionsFrame, Measure
from gui import GUI


################################################################################
# TEXTS

CURRENCY = "Kč"
WIN = 50


continuetext = "Pokračovat"
oddtext = "Liché"
eventext = "Sudé"
rolltext = "Hodit kostkou"
correcttext = "Uhodl(a)"
incorrecttext = "Neuhodl(a)"    

treatmenttext = '''{}. kolo

Rozhodněte se, zda v tomto kole na kostce padne lichý či sudý počet bodů.

Svoji volbu si zapamatujte.

Zmáčkněte tlačítko "{}".
'''.format("{}", rolltext)

treatmenttext2 = "Stanovte, zda jste uhodli a vyhráli {} {} nebo neuhodli a nevyhráli nic.".format(WIN, CURRENCY)

controltext = """{}. kolo

Rozhodněte se, zda v tomto kole na kostce padne lichý či sudý počet bodů.
"""

controltext2 = "V tomto kole jste {}"
wintext = "vyhráli {} {}.".format(WIN, CURRENCY)
losstext = "nevyhráli nic."

choicetext = """Jak jste si všimli, tento experimentální úkol nabýval dvou podob:

Zaznamenali jste, jakou stranu předpovídáte. Poté proběhl hod a následně jste se dozvěděli, zda jste vyhráli či nikoliv.
Rozhodli jste se, jakou stranu předpovídáte. Poté proběhl hod a následně jste sami určili, zda jste vyhráli či nikoliv.

Nyní proběhne posledních 10 kol úkolu. Můžete si sami vybrat, zda je chcete řešit v:
- 1. podobě  
- 2. podobě
- necháte rozhodnout náhodu, tj. s poloviční pravděpodobností budete přiřazeni do 1. podoby úkolu s poloviční pravděpodobností do 2. podoby úkolu.
"""

controlchoicetext = "1. podoba"
treatmentchoicetext = "2. podoba"
randomchoicetext = "Rozhodne náhoda"   

intro_block_1 = """
V tomto úkolu budete předpovídat, zda při virtuálním hodu kostkou nakonec padne lichý či sudý počet bodů. Virtuální kostka je generátor náhodných čísel, který se náhodě zastaví a ukáže 1, 2, 3, 4, 5 nebo 6 bodů. Liché hody jsou 1, 3 a 5. Sudé hody jsou 2, 4 a 6.

Nejprve se uskuteční 10 kol, poté nastane pauza, nato se uskuteční dalších 10 kol, nastane opět pauza a poté se uskuteční posledních 10 kol (celkem tedy budete předpovídat 30 kol hodů kostkou). 

Za každou správnou předpověď, zda padne sudý či lichý počet bodů, získáte na konci experimentu {} {}. Kdybyste uhodli všechny hody získáte tedy {} {}, když neuhodnete žádný, nezískáte v tomto úkolu nic.
""".format(WIN, CURRENCY, WIN*30, CURRENCY)

intro_block_2 = """
Tímto skončilo prvních 10 kol. Bude-li tento blok kol vylosován, získáte odměnu {} {}. Nyní proběhne druhých 10 kol.
""".format("{}", CURRENCY)

intro_block_3 = """
Intro3
"""

endtext = """
Tímto část experimentu s hádáním bodů na kostce končí.
Náhodně byl vybrán k vyplacení blok {}.
Vydělali jste si tedy {} {}.
"""

debrieftext = """
Jak již bylo zmíněno, experimentální úkol nabýval dvou podob:

Zaznamenali jste, jakou stranu předpovídáte. Poté proběhl hod a následně jste se dozvěděli, zda jste vyhráli či nikoliv.

Rozhodli jste se, jakou stranu předpovídáte. Poté proběhl hod a následně jste sami určili, zda jste vyhráli či nikoliv.

Please rate how much do you agree for each versions of the task that with several characterizations.
"""

debriefquest1 = "How much do you agree for the first version that ..."
debriefquest2 = "How much do you agree for the second version that ..."
debriefscale1 = "completely disagree"
debriefscale2 = "disagree"
debriefscale3 = "agree"
debriefscale4 = "compeletely agree"

debriefdimensions = ["... it required attention",
                     "... it required logical thinking",
                     "... it was possible to behave immorally in it",
                     "... it was acceptable to behave immorally in it"]


################################################################################


class Cheating(ExperimentFrame):
    def __init__(self, root, block):
        super().__init__(root)

        #######################
        # adjustable parameters
        self.trials = 2
        self.pause_after_roll = 0.5
        self.pause_before_trial = 0.2
        self.displayNum = self.createDots # self.createDots or self.createText
        self.fakeRolling = True
        self.diesize = 240
        #######################

        global conditions
        self.condition = conditions[block - 1]
        self.blockNumber = block

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

        if block == 1:
            self.root.wins = [0, 0, 0]            

        self.responses = []


    def run(self):
        self.bottomText["state"] = "disabled"
        self.upperText["state"] = "disabled"
        if self.currentTrial < self.trials:
            self.currentTrial += 1
            self.startTrial()
        else:
            if self.blockNumber == 1:
                self.root.texts["win1"] = self.root.wins[self.blockNumber - 1] * WIN
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
        if "treatment" in self.condition:
            self.upperText.insert("1.0", treatmenttext.format(self.currentTrial))
            self.rollButton = ttk.Button(self.upperButtonFrame, text = rolltext,
                                         command = self.roll)
            self.rollButton.grid(row = 0, column = 1)
        elif "control" in self.condition:
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
        if "treatment" in self.condition:
            self.bottomText.insert("1.0", treatmenttext2)
            self.winButton = ttk.Button(self.bottomButtonFrame, text = correcttext,
                                         command = lambda: self.answer("win"))
            self.lossButton = ttk.Button(self.bottomButtonFrame, text = incorrecttext,
                                        command = lambda: self.answer("loss"))
            self.winButton.grid(row = 0, column = 0, padx = 30)
            self.lossButton.grid(row = 0, column = 2, padx = 30)
        elif "control" in self.condition:
            win = (self.response == "odd" and self.currentRoll in (1,3,5)) or (
                self.response == "even" and self.currentRoll in (2,4,6))
            if win:
                self.root.wins[self.blockNumber - 1] += 1
            text = wintext if win else losstext
            self.bottomText.insert("1.0", controltext2.format(text))
            self.continueButton = ttk.Button(self.bottomButtonFrame, text = continuetext,
                                             command = self.answer)
            self.continueButton.grid(row = 0, column = 1)
        self.bottomText["state"] = "disabled"


    def roll(self, response = "NA"):
        self.firstResponse = perf_counter()
        if "treatment" in self.condition:
            self.rollButton["state"] = "disabled"
        else:
            self.evenButton["state"] = "disabled"
            self.oddButton["state"] = "disabled"
        self.die.create_rectangle((5, 5, self.diesize - 5, self.diesize - 5),
                                  fill = "white", tag = "die", outline = "black", width = 5)
        # fake rolling
        if self.fakeRolling:
            for roll in range(random.randint(4,6)):         
                self.displayNum(self.diesize/2, self.diesize/2, random.randint(1, 6))
                self.update()
                sleep(0.2)
                self.die.delete("dots")
        self.currentRoll = random.randint(1, 6)
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
            self.die.create_oval(tuple(coords), fill = "black", tag = "dots")


    def createText(self, x0, y0, num):
        self.die.create_text(x0, y0, text = str(num), font = "helvetica 70", tag = "die")


    def answer(self, answer = "NA"):
        t = perf_counter()
        if answer == "win":
                self.root.wins[self.blockNumber - 1] += 1
        self.responses.append([self.blockNumber, self.currentTrial, self.condition,
                               self.currentRoll, self.response,
                               answer, t - self.time, self.firstResponse - self.time,
                               t - self.beforeSecondResponse])
        self.bottomText["state"] = "normal"
        self.upperText["state"] = "normal"
        self.die.delete("die")
        self.die.delete("dots")
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



class Selection(InstructionsFrame):
    def __init__(self, root):
        super().__init__(root, text = choicetext, proceed = False)

        ttk.Style().configure("TButton", font = "helvetica 15", width = 16)

        self.control = ttk.Button(self, text = controlchoicetext,
                                  command = lambda: self.response("control"))
        self.treatment = ttk.Button(self, text = treatmentchoicetext,
                                    command = lambda: self.response("treatment"))
        self.random = ttk.Button(self, text = randomchoicetext,
                                 command = lambda: self.response("random"))
        self.control.grid(row = 2, column = 0)
        self.random.grid(row = 2, column = 1)
        self.treatment.grid(row = 2, column = 2)        

    def response(self, choice):
        global conditions
        conditions[2] += "_" + choice
        if choice == "random":
            if random.random() < 0.5:
                conditions[2] += "_" + "treatment"
            else:
                conditions[2] += "_" + "control"
        self.nextFun()



class EndCheating(InstructionsFrame):
    def __init__(self, root):
        block = random.randint(1, 3)
        text = endtext.format(block, root.wins[block-1] * WIN, CURRENCY)
        super().__init__(root, text = text, width = 60)


        
class DebriefCheating(ExperimentFrame):
    def __init__(self, root):
        super().__init__(root)

        self.text = Text(self, height = 10, width = 90, relief = "flat", font = "helvetica 15")
        self.text.insert("1.0", debrieftext)
        self.text["state"] = "disabled"
        self.text.grid(row = 1, column = 1)

        self.frame1 = OneFrame(self, debriefquest1)
        self.frame1.grid(row = 2, column = 1)

        self.frame2 = OneFrame(self, debriefquest2)
        self.frame2.grid(row = 3, column = 1)            

        ttk.Style().configure("TButton", font = "helvetica 15")
        self.next = ttk.Button(self, text = continuetext, command = self.nextFun,
                               state = "disabled")
        self.next.grid(row = 4, column = 1, sticky = N)

        self.rowconfigure(0, weight = 1)
        self.rowconfigure(1, weight = 1)
        self.rowconfigure(2, weight = 1)
        self.rowconfigure(3, weight = 1)
        self.rowconfigure(4, weight = 2)
        self.columnconfigure(0, weight = 1)
        self.columnconfigure(2, weight = 1)

    def check(self):
        if self.frame1.check() and self.frame2.check():
            self.next["state"] = "!disabled"
            return True

    def write(self):
        if self.check():
            self.file.write("Perception cheating\n" + self.id + "\t")
            self.frame1.write()
            self.file.write("\t")
            self.frame2.write()
            self.file.write("\n")



class OneFrame(Canvas):
    def __init__(self, root, question):
        super().__init__(root, background = "white", highlightbackground = "white",
                         highlightcolor = "white")

        self.root = root
        self.file = self.root.file

        self.answers = [debriefscale1, debriefscale2, debriefscale3, debriefscale4]
        
        self.lab1 = ttk.Label(self, text = question, font = "helvetica 15", background = "white")
        self.lab1.grid(row = 2, column = 1, pady = 10)
        self.measures = []
        for count, word in enumerate(debriefdimensions):
            self.measures.append(Measure(self, word, self.answers, "", "", function = self.root.check,
                                         labelPosition = "none"))
            self.measures[count].grid(row = count + 3, column = 1, columnspan = 2, sticky = E)

    def check(self):
        for measure in self.measures:
            if not measure.answer.get():
                return False
        else:
            return True             

    def write(self):
        for measure in self.measures:
            self.file.write(str(self.answers.index(measure.answer.get()) + 1))
            self.file.write("\t")
     
            

        
conditions = ["treatment", "control"]
random.shuffle(conditions)
if random.random() < 0.5:
    if random.random() < 0.5:
        conditions.append("treatment")
    else:
        conditions.append("control")
else:
    conditions.append("choice")

Instructions1 = (InstructionsFrame, {"text": intro_block_1, "height": 12})
Instructions2 = (InstructionsFrame, {"text": intro_block_2, "height": 5, "update": ["win1"]})
if conditions[2] == "choice":
    Instructions3 = Selection
else:
    Instructions3 = (InstructionsFrame, {"text": intro_block_3, "height": 5})

BlockOne = (Cheating, {"block": 1})
BlockTwo = (Cheating, {"block": 2})
BlockThree = (Cheating, {"block": 3})



if __name__ == "__main__":
    os.chdir(os.path.dirname(os.getcwd()))
    GUI([Instructions1,
         BlockOne,
         Instructions2,
         BlockTwo,
         Instructions3,
         BlockThree,
         EndCheating,
         DebriefCheating
         ])
