from pick import pick
from time import sleep
from parser.INAJOG import INAJOG as inajog
from parser.kespro import KesPro
from parser.jurkeb import JurKep
from parser.jkp import JKP
from parser.jri import JRI
from parser.radiationoncology import RadiationOncology

def main():
    title = "Please select journal:"
    options = [
            "Journal of Reproduction & Infertility", #0
            "Radiation Oncology", #1
            "INAJOG", #2
            "Jurnal Kesehatan Reproduksi", #3
            "Jurnal Kebidanan", #4
            "Jurnal Ners dan Kebidanan", #5
            "Jurnal Keperawatan Pajajaran", #6
            "⛔ quit"
        ]

    selected, index = pick(options, title)

    if selected == "⛔ quit":
        print("Bye!")
        exit()

    if index == 0:
        JRI(selected, "https://www.jri.ir/en/archive")
    elif index == 1:
        RadiationOncology(selected, "https://link.springer.com/journal/13014/volumes-and-issues")
    elif index == 2:
        inajog(selected, "http://www.inajog.com/index.php/journal/issue/archive")
    elif index == 3:
        KesPro(selected, "https://ejournal2.litbang.kemkes.go.id/index.php/kespro/issue/archive")
    elif index == 4:
        JurKep(selected, "https://ejournal.poltekkes-smg.ac.id/ojs/index.php/jurkeb/issue/archive")
    elif index == 5:
        JurKep(selected, "http://jnk.phb.ac.id/index.php/jnk/issue/archive")
    elif index == 6:
        JKP(selected, "http://jkp.fkep.unpad.ac.id/index.php/jkp/issue/archive")

    # reselect journal
    sleep(2)
    main()

if __name__ == "__main__":
    main()