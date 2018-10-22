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

Please write down the number of your workstation in the box:

Please, do not continue with the study until you are asked to by a research assistant. 
"""



endingtext = """
Děkujeme za Vaši účast!

Prosíme, abyste informace o těchto experimentech nešířil(a) během následujících 3 měsíců. Zejména Vás žádáme, abyste tyto informace nešířil(a) mezi potenciální účastníky a účastnice těchto experimentů. 

{}

Nyní si můžete vzít své věci a přejít do vedlejší místnosti, kde Vám bude vyplacena odměna. 
Tím Vaše účast na dnešní studii končí. Ještě jednou děkujeme!
"""

winending = "V loterii jste byl(a) vylosován(a) a z vybraných produktů si tedy jako výhru tři odnesete. Z výrobků, které jste si vybral(a), byly tři náhodně vylosovány. Na papírek ležící na stole napište číslo Vašeho pracovního místa a níže uvedené kódy vyhraných produktů:\n{}  {}  {}\nPro případ, že by tyto produkty nebyly v zásobách, si prosím zapište také tyto kódy náhradních produktů:\n{}  {}  {}\n\nPapírek si s sebou vezměte a předejte ho experimentátorovi."
lostending = "V loterii jste nebyl(a) vylosován/a a bohužel si tedy domů vybrané produkty neodnesete. Dostanete však samozřejmě svou řádnou odměnu za účast v experimentu."
################################################################################



Intro = (InstructionsFrame, {"text": intro})


class Ending(InstructionsFrame):
    def __init__(self):
        pass
    
    def __call__(self, root):
        win = random.random() < 1/8
        if win and hasattr(root, "selected"):
            keys = [key for key in root.selected.keys()]
            keys = random.sample(keys, 6)
            prize = []
            for key in keys:
                prize.append(str(int(key) + (int(random.choice(root.selected[key])) - 1)*16))
            root.file.write("Won products\n" + "\n".join(prize))
            text = endingtext.format(winending.format(*prize))
        else:
            text = endingtext.format(lostending)
        super().__init__(root, text, height = 30, font = 15, proceed = False)
        return self

ending = Ending()
