from common import InstructionsFrame
from math import ceil
import random

################################################################################
# TEXTS
intro = """
Welcome to the research study conducted in cooperation with the Faculty of Business Administration at the University of Economics, Prague. The study consists of several different tasks and questionnaires. Below you see a basic outline of the study:

1) Dice rolling task: You will predict whether odd or even number will be rolled on a die. You will make predictions for 3 sets consisting of 10 trials each. You can earn money in this part.
2) Lottery task: You will choose a lottery. You can earn money depending on the outcome of the chosen lottery.
3) Distribution of money: You will learn how much you have earned in the previous parts and you can decide what to do with your earnings.
4) Questionnaires: You will answer questions about your characteristics and attitudes. There will be items checking whether you pay attention to the questions. If you answer these attention checks correctly, you can earn additional money.
5) End of the study and payment: After you are finished, you can go to the next room where you signed a contract based on which you will receive all your money into your bank account. Because only the overall sum will be in the contract, nobody will know how much money did you earn in different parts of the study or how did you decide to distribute it.  

Thank you for turning off your mobile phones completely and please do not communicate with others in any way during the study. In case you are communicating with other participants or disturbing the study in any other way, you will be asked to leave the laboratory without payment.

In case you have any questions or you encounter any technical difficulties during the task, just raise your hand and wait for a research assistant.

Please, do not continue with the study until you are asked to by a research assistant. 
"""



endingtext = """
Výsledky experimentu budou po vyhodnocení a publikování volně dostupné na webových stránkách laboratoře a na serveru https://osf.io/. Prosíme Vás, abyste o výzkumu nemluvili s dalšími potenciálními účastníky, aby tak nebyly ovlivněny jejich odpovědi a chování. Přihlaste se rukou, experimentátor přijde a experiment ukončí.

Poté si prosím vezměte všechny své osobní věci a tak, abyste nerušili ostatní účastníky, se odeberte do vedlejší místnosti, kde Vám bude vyplacena odměna.

Tímto celý experiment končí, děkujeme Vám za účast! 
 
Pracovníci laboratoří CEBEX / PLESS  
"""

################################################################################



Intro = (InstructionsFrame, {"text": intro, "keys": ["g", "G"], "proceed": False, "height": 25})
Ending = (InstructionsFrame, {"text": endingtext, "keys": ["g", "G"], "proceed": False, "height": 10})
