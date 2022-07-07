from pick import pick
from time import sleep
from parser.INAJOG import INAJOG
from parser.kespro import KesPro
from parser.jurkeb import JurKep
from parser.jkp import JKP
from parser.jri import JRI
from parser.radiationoncology import RadiationOncology

def main():
    parsers = {
        "Journal of Reproduction & Infertility": (JRI, "https://www.jri.ir/en/archive"),
        "Radiation Oncology": (RadiationOncology, "https://link.springer.com/journal/13014/volumes-and-issues"),
        "INAJOG": (INAJOG, "http://www.inajog.com/index.php/journal/issue/archive"),
        "Jurnal Kesehatan Reproduksi": (KesPro, "https://ejournal2.litbang.kemkes.go.id/index.php/kespro/issue/archive"),
        "Jurnal Kebidanan": (JurKep, "https://ejournal.poltekkes-smg.ac.id/ojs/index.php/jurkeb/issue/archive"),
        "Jurnal Ners dan Kebidanan": (JurKep, "http://jnk.phb.ac.id/index.php/jnk/issue/archive"),
        "Jurnal Keperawatan Pajajaran": (JKP, "http://jkp.fkep.unpad.ac.id/index.php/jkp/issue/archive"),
    }

    title = "Please select journal:"
    options = [p for p in sorted(parsers.keys())]
    options.append("⛔️ quit")

    selected, index = pick(options, title)

    if selected == "⛔️ quit":
        print("Bye!")
        exit()

    # run parser
    cls, url = parsers[selected]
    cls(selected, url)

    # reselect journal
    sleep(2)
    main()

if __name__ == "__main__":
    main()