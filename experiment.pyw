#! python3

import sys
import os

sys.path.append(os.path.join(os.getcwd(), "Stuff"))


from gui import GUI

from questionnaire import Work
from quest import QuestInstructions, Hexaco, Prosociality
from intros import ending, Intro, Debriefing
from comments import Comments
from demo import Demographics
from cheating import Instructions1, BlockOne, Instructions2, BlockTwo, Instructions3, BlockThree


frames = [#Intro,
          Instructions1,
          BlockOne,
          Instructions2,
          BlockTwo,
          Instructions3,
          BlockThree,
          QuestInstructions,
          Hexaco,
          Prosociality,
          Work,
          Demographics

          #ChoiceBlindnessInstructions3, # debriefing for choice blindness
          #DebriefingOne,
          #DebriefingTwo,
          #Comments,
          #Debriefing,
          #ending
         ]



with open("start.txt") as f:
    startingFrame = f.readline().strip()
    frames = frames[int(startingFrame):]
    
GUI(frames)

text = ""
with open("start.txt") as f:
    for num, line in enumerate(f):
        if num == 0:
            text += "0\n"
        else:
            text += line

with open("start.txt", mode = "w") as f:
    f.write(text)