#! python3
from tkinter import *
from tkinter import ttk

import os

from common import ExperimentFrame
from gui import GUI
from constants import CURRENCY


class Demographics(ExperimentFrame):
    def __init__(self, root):
        super().__init__(root)
       
        self.sex = StringVar()
        self.language = StringVar()
        self.age = StringVar()
        self.student = StringVar()
        self.field = StringVar()
        self.field.set("Nestuduji VŠ")
        self.education = StringVar()
        self.religion = StringVar()

        self.lab1 = ttk.Label(self, text = "Pohlaví:", background = "white",
                              font = "helvetica 15")
        self.lab1.grid(column = 1, row = 1, pady = 2, sticky = W, padx = 2)
        self.lab2 = ttk.Label(self, text = "Věk:", background = "white",
                              font = "helvetica 15")
        self.lab2.grid(column = 1, row = 2, pady = 2, sticky = W, padx = 2)        
        self.lab3 = ttk.Label(self, text = "Mateřský jazyk:  ", background = "white",
                              font = "helvetica 15")
        self.lab3.grid(column = 1, row = 3, pady = 2, sticky = W, padx = 2)
        self.lab5 = ttk.Label(self, text = "Studujete VŠ?  ", background = "white",
                              font = "helvetica 15")
        self.lab5.grid(column = 1, row = 5, pady = 2, sticky = W, padx = 2)
        self.lab6 = ttk.Label(self, text = "Pokud ano, jaký obor? ", background = "white",
                              font = "helvetica 15")
        self.lab6.grid(column = 1, row = 6, pady = 2, sticky = W, padx = 2)
        self.lab7 = ttk.Label(self, text = "Jaké je vaše nejvyšší dosažené vzdělání? ", background = "white",
                              font = "helvetica 15")
        self.lab7.grid(column = 1, row = 7, pady = 2, sticky = W, padx = 2)
        self.lab8 = ttk.Label(self, text = "Jste věřící? ", background = "white",
                              font = "helvetica 15")
        self.lab8.grid(column = 1, row = 8, pady = 2, sticky = W, padx = 2)

        
        self.male = ttk.Radiobutton(self, text = "muž", variable = self.sex, value = "male",
                                    command = self.checkAllFilled)
        self.female = ttk.Radiobutton(self, text = "žena", variable = self.sex,
                                      value = "female", command = self.checkAllFilled)

        self.czech = ttk.Radiobutton(self, text = "český", variable = self.language,
                                     value = "czech", command = self.checkAllFilled)
        self.slovak = ttk.Radiobutton(self, text = "slovenský", variable = self.language,
                                     value = "slovak", command = self.checkAllFilled)
        self.other = ttk.Radiobutton(self, text = "jiný", variable = self.language,
                                     value = "other", command = self.checkAllFilled)

        self.yes = ttk.Radiobutton(self, text = "ano", variable = self.student,
                                     value = "student", command = self.checkAllFilled)
        self.no = ttk.Radiobutton(self, text = "ne", variable = self.student,
                                    value = "nostudent", command = self.checkAllFilled)


        ttk.Style().configure("TRadiobutton", background = "white", font = "helvetica 15")
        ttk.Style().configure("TButton", font = "helvetica 15")

        self.ageCB = ttk.Combobox(self, textvariable = self.age, width = 6, font = "helvetica 14",
                                  state = "readonly")
        self.ageCB["values"] = tuple([""] + [str(i) for i in range(18, 80)])
        self.ageCB.bind("<<ComboboxSelected>>", lambda e: self.checkAllFilled())

        self.fieldCB = ttk.Combobox(self, textvariable = self.field, width = 15,
                                    font = "helvetica 14", state = "readonly")
        self.fieldCB["values"] = ["Nestuduji VŠ",
                                  "Ekonomie / management",
                                  "Jazyky / mezinárodní studia",
                                  "Kultura / umění",
                                  "Medicína / farmacie",
                                  "Právo / veřejná správa",
                                  "Přírodní vědy",
                                  "Technika / informatika",
                                  "Učitelství / sport",
                                  "Zemědělství / veterina",
                                  "Humanitní / společenské vědy",
                                  "Jiné"]
        self.fieldCB.bind("<<ComboboxSelected>>", lambda e: self.checkAllFilled())

        self.educationCB = ttk.Combobox(self, textvariable = self.education, width = 22,
                                    font = "helvetica 14", state = "readonly")
        self.educationCB["values"] = ["Žádné formální vzdělání",
                                      "Ukončené základní vzdělání",
                                      "Ukončené středoškolské vzdělání",
                                      "Neukončené vysokoškolské vzdělání",
                                      "Ukončené vysokoškolské vzdělání",
                                      "Ukončené doktorské vzdělání"]
        self.educationCB.bind("<<ComboboxSelected>>", lambda e: self.checkAllFilled())

        self.religionCB = ttk.Combobox(self, textvariable = self.religion, width = 40,
                                       font = "helvetica 14", state = "readonly")
        self.religionCB["values"] = ["Ano, jsem aktivním členem/členkou nějaké církve nebo náboženského společenství",
                                     "Ano, jsem pasivním členem/členkou nějaké církve nebo náboženského společenství",
                                     "Ano, ale nejsem členem/členkou církve nebo společenství",
                                     "Nevím",
                                     "Ne"]
        self.religionCB.bind("<<ComboboxSelected>>", lambda e: self.checkAllFilled())        

        self.male.grid(column = 2, row = 1, pady = 7, padx = 7, sticky = W)
        self.female.grid(column = 3, row = 1, pady = 7, padx = 7, sticky = W)
        self.czech.grid(column = 2, row = 3, pady = 7, padx = 7, sticky = W)
        self.slovak.grid(column = 3, row = 3, pady = 7, padx = 7, sticky = W)
        self.other.grid(column = 4, row = 3, pady = 7, padx = 45, sticky = W)
        self.ageCB.grid(column = 2, row = 2, pady = 7, padx = 7, sticky = W)
        self.yes.grid(column = 2, row = 5, pady = 7, padx = 7, sticky = W)
        self.no.grid(column = 3, row = 5, pady = 7, padx = 7, sticky = W)    
        self.fieldCB.grid(column = 2, columnspan = 2, row = 6, pady = 7, padx = 7, sticky = W)
        self.educationCB.grid(column = 2, columnspan = 3, row = 7, pady = 7, padx = 7, sticky = W)
        self.religionCB.grid(column = 2, columnspan = 3, row = 8, pady = 7, padx = 7, sticky = W)

        self.columnconfigure(5, weight = 1)
        self.columnconfigure(0, weight = 1)
        self.rowconfigure(0, weight = 1)
        self.rowconfigure(11, weight = 1)

        self.writeWinnings()

        self.next = ttk.Button(self, text = "Pokračovat", command = self.nextFun,
                               state = "disabled")
        self.next.grid(row = 11, column = 1, pady = 15, columnspan = 3)


    def checkAllFilled(self, _ = None):
        if all([v.get() for v in [self.language, self.age, self.sex, self.field, self.student,
                                  self.education, self.religion]]):
            self.next["state"] = "!disabled"


    def writeWinnings(self):
        options = os.path.join(os.path.dirname(os.path.dirname(__file__)), "options.txt")
        if os.path.exists(options):
            with open(options, mode = "r") as f:
                directory = f.readline().strip()
                station = f.readline().strip()
        else:
            directory = os.path.dirname(self.root.outputfile)
            station = "UNKNOWN"
        filename = os.path.splitext(os.path.basename(self.root.outputfile))[0]
        output = os.path.join(directory, filename + "_STATION_" + str(station) + ".txt")
        # pridat attention check
        if all([key in self.root.texts for key in ["dice", "charity", "donation", "lottery_win"]]):
            dice = self.root.texts["dice"]
            charity = self.root.texts["charity"]
            donation = self.root.texts["donation"]
            lottery = self.root.texts["lottery_win"]
            with open(output, mode = "w", encoding="utf-8") as infile:
                infile.write("reward: " + str(dice + lottery - donation) + CURRENCY + "\n\n")
                infile.write(charity + ": " + str(donation) + CURRENCY + "\n\n")
                infile.write("dice: " + str(dice) + CURRENCY + "\n")
                infile.write("lottery: " + str(lottery) + CURRENCY)
        

    def write(self):
        self.root.texts ["gender"] = self.sex.get()
        self.file.write("Demographics\n")
        self.file.write("\t".join([self.id, self.sex.get(), self.age.get(), self.language.get(),
                                   self.student.get(), self.field.get(),
                                   self.education.get()]) + "\n")


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.getcwd()))
    GUI([Demographics])
