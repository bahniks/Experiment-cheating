#! python3

import sys
import os

sys.path.append(os.path.join(os.getcwd(), "Stuff"))


from gui import GUI

from questionnaire import Prosociality, Values1, Values2, Values3
from quest import QuestInstructions, Hexaco, BIDR, Agency, Disengagement, Work
from intros import ending, Intro
from comments import Comments
from demo import Demographics
from cheating import Instructions1, BlockOne, Instructions2, BlockTwo, Instructions3, BlockThree
from cheating import EndCheating, DebriefCheating
from debriefing import Debriefing


frames = [Intro,
          Instructions1,
          BlockOne,
          Instructions2,
          BlockTwo,
          Instructions3,
          BlockThree,
          EndCheating,
          DebriefCheating,
          QuestInstructions,
          Hexaco,
          BIDR,
          Agency,
          Disengagement,
          Prosociality,
          Work,
          Demographics,
          Values1,
          Values2,
          Values3,
          Debriefing
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
