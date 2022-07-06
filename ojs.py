import re
import os
from pick import pick
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from dateutil.parser import parse
from rich.console import Console

console = Console()

def init(url, name):
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    html_page = urlopen(req).read()
    link, issue = selectIssue(html_page)
    articles = getLink(link)
    # crate output folder
    year = issue[-4:]
    path = os.path.join("output", name, str(year), issue)
    console.log(path)
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=False)
    # download file
    with console.status("[bold green]Downloading...") as status:
        n = 0
        while articles:
            article = articles.pop(0)
            download(article, os.path.join(path, f"{n}.pdf"))
            console.log(f"{article} downloaded")
            n += 1

def selectIssue(html_page):
    soup = BeautifulSoup(html_page, 'lxml')
    issues = soup.find_all("a", class_="title", href=True)
    issueLink = [e['href'] for e in issues]
    issueTexts = [re.sub(r"\s+", " ", e.getText()).strip() for e in issues]
    selected, index = pick(issueTexts, "Select issue:")
    return (issueLink[index], selected)

def getLink(url):
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    html_page = urlopen(req).read()
    soup = BeautifulSoup(html_page, 'lxml')
    articles = [a['href'].replace('/view/', '/download/')
                for a in soup.find_all("a", class_="obj_galley_link pdf", href=True)]
    return articles

def download(url, path):
    response = urlopen(url)
    file = open(path, "wb")
    file.write(response.read())
    file.close()
