from pick import pick
from time import sleep
from parser.INAJOG import INAJOG
from parser.kespro import KesPro
from parser.jurkeb import JurKep
from parser.jkp import JKP
from parser.jri import JRI
from parser.radiationoncology import RadiationOncology
from parser.mji import MJI

def main():
    parsers = {
        "Journal of Reproduction & Infertility": (JRI, "https://www.jri.ir/en/archive"),
        "Radiation Oncology": (RadiationOncology, "https://link.springer.com/journal/13014/volumes-and-issues"),
        "INAJOG": (INAJOG, "http://www.inajog.com/index.php/journal/issue/archive"),
        "Jurnal Kesehatan Reproduksi": (KesPro, "https://ejournal2.litbang.kemkes.go.id/index.php/kespro/issue/archive"),
        "Jurnal Kebidanan": (JurKep, "https://ejournal.poltekkes-smg.ac.id/ojs/index.php/jurkeb/issue/archive"),
        "Jurnal Ners dan Kebidanan": (JurKep, "http://jnk.phb.ac.id/index.php/jnk/issue/archive"),
        "Jurnal Keperawatan Pajajaran": (JKP, "http://jkp.fkep.unpad.ac.id/index.php/jkp/issue/archive"),
        "Medical Journal of Indonesia": (MJI, "https://mji.ui.ac.id/journal/index.php/mji/issue/archive"),
        "Majalah Kedokteran Bandung": (JurKep, "http://journal.fk.unpad.ac.id/index.php/mkb/issue/archive"),
        "Acta Medica Indonesiana": (JurKep, "http://www.actamedindones.org/index.php/ijim/issue/archive"),
        "Jurnal Media Analis Kesehatan": (JurKep, "https://journal.poltekkes-mks.ac.id/ojs2/index.php/mediaanalis/issue/archive"),
        "Indonesian Journal of Chemistry": (JurKep, "https://jurnal.ugm.ac.id/ijc/issue/archive"),
        "Jurnal Kesehatan Gigi": (JurKep, "https://ejournal.poltekkes-smg.ac.id/ojs/index.php/jkg/issue/archive"),
        "Dental Journal (Majalah Kedokteran Gigi)": (MJI, "https://e-journal.unair.ac.id/MKG/issue/archive"),
        "Media Kesehatan Gigi": (JurKep, "https://journal.poltekkes-mks.ac.id/ojs2/index.php/mediagigi/issue/archive"),
        "LINK Poltekkes Semarang": (JurKep, "https://ejournal.poltekkes-smg.ac.id/ojs/index.php/link/issue/archive"),
        "Jurnal Gizi Indonesia": (JurKep, "https://ejournal.undip.ac.id/index.php/jgi/issue/archive"),
        "Jurnal Gizi Klinik Indonesia": (JurKep, "https://jurnal.ugm.ac.id/jgki/issue/archive"),
        "Jurnal Teknologi dan Industri Pangan": (MJI, "https://jurnal.ipb.ac.id/index.php/jtip/issue/archive"),
        "Media Gizi Indonesia": (MJI, "https://e-journal.unair.ac.id/MGI/issue/archive"),
        "Media Gizi Mikro Indonesia": (MJI, "https://ejournal2.litbang.kemkes.go.id/index.php/mgmi/issue/archive"),
        "Media Penelitian dan Pengembangan Kesehatan": (INAJOG, "https://ejournal2.litbang.kemkes.go.id/index.php/mgmi/issue/archive"),
        "Universa Medicina": (INAJOG, "https://ejournal2.litbang.kemkes.go.id/index.php/mgmi/issue/archive"),
        "Jurnal Imejing Diagnostik (JImeD)": (JurKep, "https://ejournal.poltekkes-smg.ac.id/ojs/index.php/jimed/issue/archive"),
        "Jurnal Keperawatan Soedirman": (JurKep, "https://www.jks.fikes.unsoed.ac.id/index.php/jks/issue/archive"),
        "Jurnal Ners": (MJI, "https://e-journal.unair.ac.id/JNERS/issue/archive"),
        "Jurnal Aspirator": (MJI, "https://ejournal2.litbang.kemkes.go.id/index.php/aspirator/issue/archive"),
        "Jurnal Ekologi Kesehatan": (MJI, "https://ejournal2.litbang.kemkes.go.id/index.php/jek/issue/archive"),
        "Jurnal Vektor Penyakit": (MJI, "http://ejournal2.litbang.kemkes.go.id/index.php/vektorp/issue/archive"),
        "Nurse Media Journal of Nursing": (JurKep, "https://ejournal.undip.ac.id/index.php/medianers/issue/archive"),
        "Jurnal Kesehatan Prima": (JurKep, "http://jkp.poltekkes-mataram.ac.id/index.php/home/issue/archive"),
        "Jurnal Manajemen Informasi Kesehatan Indonesia": (JurKep, "https://jmiki.aptirmik.or.id/index.php/jmiki/issue/archive"),
        "Jurnal Riset Kesehatan": (JurKep, "https://ejournal.poltekkes-smg.ac.id/ojs/index.php/jrk/issue/archive"),
        "Diponegoro Journal of Management": (JurKep, "https://ejournal3.undip.ac.id/index.php/djom/issue/archive"),
        "Jurnal Rekam Medis dan Informasi Kesehatan": (JurKep, "https://ejournal.poltekkes-smg.ac.id/ojs/index.php/RMIK/issue/archive"),
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