import inquirer
from time import sleep
from parser.INAJOG import INAJOG
from parser.kespro import KesPro
from parser.jri import JRI
from parser.radiationoncology import RadiationOncology
from parser.ojs2 import Ojs2
from parser.ojs3 import Ojs3

def main():
    parsers = {
        "Journal of Reproduction & Infertility": (JRI, "https://www.jri.ir/en/archive"),
        "Radiation Oncology": (RadiationOncology, "https://link.springer.com/journal/13014/volumes-and-issues"),
        "INAJOG": (INAJOG, "http://www.inajog.com/index.php/journal/issue/archive"),
        "Jurnal Kesehatan Reproduksi": (KesPro, "https://ejournal2.litbang.kemkes.go.id/index.php/kespro/issue/archive"),
        "Jurnal Kebidanan": (Ojs2, "https://ejournal.poltekkes-smg.ac.id/ojs/index.php/jurkeb/issue/archive"),
        "Jurnal Ners dan Kebidanan": (Ojs2, "http://jnk.phb.ac.id/index.php/jnk/issue/archive"),
        "Jurnal Keperawatan Pajajaran": (Ojs3, "http://jkp.fkep.unpad.ac.id/index.php/jkp/issue/archive"),
        "Medical Journal of Indonesia": (Ojs3, "https://mji.ui.ac.id/journal/index.php/mji/issue/archive"),
        "Majalah Kedokteran Bandung": (Ojs2, "http://journal.fk.unpad.ac.id/index.php/mkb/issue/archive"),
        "Acta Medica Indonesiana": (Ojs2, "http://www.actamedindones.org/index.php/ijim/issue/archive"),
        "Jurnal Media Analis Kesehatan": (Ojs2, "https://journal.poltekkes-mks.ac.id/ojs2/index.php/mediaanalis/issue/archive"),
        "Indonesian Journal of Chemistry": (Ojs2, "https://jurnal.ugm.ac.id/ijc/issue/archive"),
        "Jurnal Kesehatan Gigi": (Ojs2, "https://ejournal.poltekkes-smg.ac.id/ojs/index.php/jkg/issue/archive"),
        "Dental Journal (Majalah Kedokteran Gigi)": (Ojs3, "https://e-journal.unair.ac.id/MKG/issue/archive"),
        "Media Kesehatan Gigi": (Ojs2, "https://journal.poltekkes-mks.ac.id/ojs2/index.php/mediagigi/issue/archive"),
        "LINK Poltekkes Semarang": (Ojs2, "https://ejournal.poltekkes-smg.ac.id/ojs/index.php/link/issue/archive"),
        "Jurnal Gizi Indonesia": (Ojs2, "https://ejournal.undip.ac.id/index.php/jgi/issue/archive"),
        "Jurnal Gizi Klinik Indonesia": (Ojs2, "https://jurnal.ugm.ac.id/jgki/issue/archive"),
        "Jurnal Teknologi dan Industri Pangan": (Ojs3, "https://jurnal.ipb.ac.id/index.php/jtip/issue/archive"),
        "Media Gizi Indonesia": (Ojs3, "https://e-journal.unair.ac.id/MGI/issue/archive"),
        "Media Gizi Mikro Indonesia": (Ojs3, "https://ejournal2.litbang.kemkes.go.id/index.php/mgmi/issue/archive"),
        "Media Penelitian dan Pengembangan Kesehatan": (INAJOG, "https://ejournal2.litbang.kemkes.go.id/index.php/mgmi/issue/archive"),
        "Universa Medicina": (INAJOG, "https://ejournal2.litbang.kemkes.go.id/index.php/mgmi/issue/archive"),
        "Jurnal Imejing Diagnostik (JImeD)": (Ojs2, "https://ejournal.poltekkes-smg.ac.id/ojs/index.php/jimed/issue/archive"),
        "Jurnal Keperawatan Soedirman": (Ojs2, "https://www.jks.fikes.unsoed.ac.id/index.php/jks/issue/archive"),
        "Jurnal Ners": (Ojs3, "https://e-journal.unair.ac.id/JNERS/issue/archive"),
        "Jurnal Aspirator": (Ojs3, "https://ejournal2.litbang.kemkes.go.id/index.php/aspirator/issue/archive"),
        "Jurnal Ekologi Kesehatan": (Ojs3, "https://ejournal2.litbang.kemkes.go.id/index.php/jek/issue/archive"),
        "Jurnal Vektor Penyakit": (Ojs3, "http://ejournal2.litbang.kemkes.go.id/index.php/vektorp/issue/archive"),
        "Nurse Media Journal of Nursing": (Ojs2, "https://ejournal.undip.ac.id/index.php/medianers/issue/archive"),
        "Jurnal Kesehatan Prima": (Ojs2, "http://jkp.poltekkes-mataram.ac.id/index.php/home/issue/archive"),
        "Jurnal Manajemen Informasi Kesehatan Indonesia": (Ojs2, "https://jmiki.aptirmik.or.id/index.php/jmiki/issue/archive"),
        "Jurnal Riset Kesehatan": (Ojs2, "https://ejournal.poltekkes-smg.ac.id/ojs/index.php/jrk/issue/archive"),
        "Diponegoro Journal of Management": (Ojs2, "https://ejournal3.undip.ac.id/index.php/djom/issue/archive"),
        "Jurnal Rekam Medis dan Informasi Kesehatan": (Ojs2, "https://ejournal.poltekkes-smg.ac.id/ojs/index.php/RMIK/issue/archive"),
    }

    title = "Please select journal:"
    options = [p for p in sorted(parsers.keys())]
    options.append("⛔️ quit")

    questions = [
        inquirer.List('journal', message=title, choices=options)
    ]
    answers = inquirer.prompt(questions)
    
    selected = answers['journal']

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