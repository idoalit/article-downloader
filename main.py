from pick import pick
import ojs

title = "Please select journal:"
options = [
        "Journal of Reproduction & Infertility",
        "Radiation Oncology",
        "INAJOG"
    ]

selected, index = pick(options, title)

if index == 2:
    ojs.init("http://www.inajog.com/index.php/journal/issue/archive", selected)