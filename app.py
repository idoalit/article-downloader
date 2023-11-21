# Mengimpor modul re, fire, json, dan inquirer
import re
import fire
import json
import signal
import inquirer
import xml.etree.ElementTree as ET
import requests
from parser.ojs2 import Ojs2
from parser.ojs3 import Ojs3
from parser.radiationoncology import RadiationOncology
from parser.jri import JRI

# exit with ctrl+c
def sigint_handler(sig, frame):
  # Print a message
  print("Received Ctrl+C, quitting...")
  exit(0)
signal.signal(signal.SIGINT, sigint_handler)

# ignore certificate error
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

class MyUtils:
    # Membuat fungsi untuk mendapatkan url dari nama item
    def get_url(items, name):
        # Mencari item yang memiliki nama yang sama dengan argumen
        for item in items:
            if item["name"] == name:
                # Mengembalikan url dari item tersebut
                return item["url"]
        # Mengembalikan None jika tidak ada item yang cocok
        return None

    def get_ojs_version(url):
        # Check if URL is OJS
        ojs_url = re.sub("index\.php.*", "dbscripts/xml/version.xml", url)
        # Get the XML data from the URL
        response = requests.get(ojs_url)
        xml_data = response.text
        # Parse the XML data using ElementTree
        root = ET.fromstring(xml_data)
        # get version
        version = None
        for child in root:
            if child.tag == "release":
                version = child.text
        return version

    # Mendapatkan parser sesuai dengan url
    def get_parser(url):
        # Define a dictionary that maps url prefixes to parser classes
        parsers = {
            "https://link.springer.com": RadiationOncology,
            "https://www.jri.ir": JRI
        }

        # Get the url prefix from the url
        url_prefix = url.split("/")[0] + "//" + url.split("/")[2]

        # Get the parser class from the dictionary, or None if not found
        parser = parsers.get(url_prefix, None)

        # Check if the parser is None
        if parser is None:
            # Check if the url is OJS
            ojs_version = MyUtils.get_ojs_version(url)
            if ojs_version.startswith("2"):
                parser = Ojs2
            elif ojs_version.startswith("3"):
                parser = Ojs3

        # Return the parser class
        return parser


# Membuat kelas untuk aplikasi CLI
class MyApp:

    # Membuat konstruktor kelas
    def __init__(self):
        # Membuat daftar item awal
        self.items = [
            {"name": "LINK Poltekkes Semarang", "url": "https://ejournal.poltekkes-smg.ac.id/ojs/index.php/link/issue/archive"},
            {"name": "Medical Journal of Indonesia", "url": "https://mji.ui.ac.id/journal/index.php/mji/issue/archive"},
            {"name": "Jurnal Rekam Medis dan Informasi Kesehatan", "url": "https://ejournal.poltekkes-smg.ac.id/ojs/index.php/RMIK/issue/archive"},
            {"name": "Diponegoro Journal of Management", "url": "https://ejournal3.undip.ac.id/index.php/djom/issue/archive"},
            {"name": "Jurnal Riset Kesehatan", "url": "https://ejournal.poltekkes-smg.ac.id/ojs/index.php/jrk/issue/archive"},
            {"name": "Jurnal Manajemen Informasi Kesehatan Indonesia", "url": "https://jmiki.aptirmik.or.id/index.php/jmiki/issue/archive"},
            {"name": "Jurnal Kesehatan Prima", "url": "http://jkp.poltekkes-mataram.ac.id/index.php/home/issue/archive"},
            {"name": "Nurse Media Journal of Nursing", "url": "https://ejournal.undip.ac.id/index.php/medianers/issue/archive"},
            {"name": "Jurnal Vektor Penyakit", "url": "http://ejournal2.litbang.kemkes.go.id/index.php/vektorp/issue/archive"},
            {"name": "Jurnal Ekologi Kesehatan", "url": "https://ejournal2.litbang.kemkes.go.id/index.php/jek/issue/archive"},
            {"name": "Jurnal Aspirator", "url": "https://ejournal2.litbang.kemkes.go.id/index.php/aspirator/issue/archive"},
            {"name": "Jurnal Ners", "url": "https://e-journal.unair.ac.id/JNERS/issue/archive"},
            {"name": "Jurnal Keperawatan Soedirman", "url": "https://www.jks.fikes.unsoed.ac.id/index.php/jks/issue/archive"},
            {"name": "Jurnal Imejing Diagnostik (JImeD)", "url": "https://ejournal.poltekkes-smg.ac.id/ojs/index.php/jimed/issue/archive"},
            {"name": "Media Gizi Indonesia", "url": "https://e-journal.unair.ac.id/MGI/issue/archive"},
            {"name": "Jurnal Teknologi dan Industri Pangan", "url": "https://jurnal.ipb.ac.id/index.php/jtip/issue/archive"},
            {"name": "Jurnal Gizi Klinik Indonesia", "url": "https://jurnal.ugm.ac.id/jgki/issue/archive"},
            {"name": "Jurnal Gizi Indonesia", "url": "https://ejournal.undip.ac.id/index.php/jgi/issue/archive"},
            {"name": "Media Kesehatan Gigi", "url": "https://journal.poltekkes-mks.ac.id/ojs2/index.php/mediagigi/issue/archive"},
            {"name": "Dental Journal (Majalah Kedokteran Gigi)", "url": "https://e-journal.unair.ac.id/MKG/issue/archive"},
            {"name": "Jurnal Kesehatan Gigi", "url": "https://ejournal.poltekkes-smg.ac.id/ojs/index.php/jkg/issue/archive"},
            {"name": "Indonesian Journal of Chemistry", "url": "https://jurnal.ugm.ac.id/ijc/issue/archive"},
            {"name": "Jurnal Media Analis Kesehatan", "url": "https://journal.poltekkes-mks.ac.id/ojs2/index.php/mediaanalis/issue/archive"},
            {"name": "Acta Medica Indonesiana", "url": "http://www.actamedindones.org/index.php/ijim/issue/archive"},
            {"name": "Majalah Kedokteran Bandung", "url": "http://journal.fk.unpad.ac.id/index.php/mkb/issue/archive"},
            {"name": "Jurnal Keperawatan Pajajaran", "url": "http://jkp.fkep.unpad.ac.id/index.php/jkp/issue/archive"},
            {"name": "Jurnal Ners dan Kebidanan", "url": "http://jnk.phb.ac.id/index.php/jnk/issue/archive"},
            {"name": "Jurnal Kebidanan", "url": "https://ejournal.poltekkes-smg.ac.id/ojs/index.php/jurkeb/issue/archive"},
            {"name": "Radiation Oncology", "url": "https://link.springer.com/journal/13014/volumes-and-issues"},
            {"name": "Journal of Reproduction & Infertility", "url": "https://www.jri.ir/en/archive"},
        ]
        # Membaca berkas json jika ada
        try:
            with open("journals.json", "r") as f:
                self.items = json.load(f)
        except FileNotFoundError:
            pass

    # Membuat fungsi untuk menampilkan menu pilihan
    def menu(self):
        # Membuat daftar pertanyaan yang berisi satu elemen bertipe "list"
        options = [p for p in sorted([item["name"] for item in self.items])]
        options.append("⛔️ quit")

        questions = [
            inquirer.List(
                "item",
                message="Pilih jurnal yang hendak kamu unduh:",
                choices=options
            )
        ]
        # Memanggil fungsi prompt dari modul inquirer dengan argumen berupa daftar pertanyaan
        answers = inquirer.prompt(questions)
        # Mengakses jawaban yang dipilih oleh pengguna dari kamus tersebut
        selected_item = answers["item"]

        if selected_item == "⛔️ quit":
            exit()

        # Menampilkan nama dan url item yang dipilih
        url = MyUtils.get_url(self.items, selected_item)
        print(
            f"Anda memilih: {selected_item} - {url}")
        parser = MyUtils.get_parser(url)
        if parser is not None:
            parser(selected_item, url)

    # Membuat fungsi untuk menambahkan item baru
    def add(self):
        # Buat pertanyaan
        questions = [
            inquirer.Text('name', message="Apa nama jurnalnya"),
            inquirer.Text('url', message="Apa URL archives-nya")
        ]
        new_item = inquirer.prompt(questions)
        # Menambahkan item baru ke daftar item
        self.items.append(new_item)
        # Menyimpan daftar item ke berkas json
        with open("journals.json", "w") as f:
            json.dump(self.items, f, indent=4)
        # Menampilkan pesan sukses
        print(
            f"Item baru berhasil ditambahkan: {new_item['name']} - {new_item['url']}")


# Membuat objek aplikasi CLI dari kelas MyApp
app = MyApp()

# Membuat antarmuka CLI dari objek app menggunakan modul fire
fire.Fire(app)
