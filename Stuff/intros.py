from common import InstructionsFrame
from math import ceil
import random

################################################################################
# TEXTS
intro = """
Vítáme Vás na výzkumu pořádaného ve spolupráci s Fakultou podnikohospodářskou Vysoké školy ekonomické v Praze. Experiment brzy začne. V rámci experimentu budete řešit několik na sobě nezávislých úkolů a odpovídat na sérii otázek. Již nyní jste získali X,- Kč jako odměnu za svou účast. Níže vidíte zjednodušené schéma průběhu dnešního experimentu:

1) Úloha s hádáním strany kostky: Ve 3 kolech hádáte zda padne lichý či sudý počet bodů. Můžete si vydělat finanční odměnu.
2) Úloha s loterií: Vyberete jednu z loterií. Můžete si vydělat další finanční odměnu.
3) Rozhodnutí o alokaci peněz.
4) Soubor otázek a úkolů na zjištění vašich vlastností a postojů. 
5) Ve vedlejší místnosti Vám bude vyplacena celková získaná odměna.

Děkujeme, že jste zcela vypnuli svůj mobilní telefon (nejen zvonění) a v průběhu experimentu s nikým nebudete komunikovat. V případě komunikace s ostatními účastníky nebo jiného narušování experimentu Vás experimentátor vyzve k ukončení Vaší účasti bez nároku na odměnu. 

V případě jakýchkoliv nejasností či problémů, prosíme, přivolejte experimentátora zvednutím ruky.  
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
