import re
from parser.Parser import Parser
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen

class Ojs3(Parser):

    def getIssue(self):
        req = Request(self.journal_url, headers={'User-Agent': 'Mozilla/5.0'})
        html_page = urlopen(req).read()
        soup = BeautifulSoup(html_page, 'lxml')
        issues = soup.find_all("a", class_="title", href=True)
        issueLink = [e['href'] for e in issues]
        series = soup.find_all("div", class_="series")
        issueTexts = [re.sub(r"\s+", " ", e.getText()).strip() for e in series]
        return (issueLink, issueTexts)

    def getLinkDownload(self, url):
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        html_page = urlopen(req).read()
        soup = BeautifulSoup(html_page, 'lxml')
        articles = [a['href'].replace('/view/', '/download/')
                    for a in soup.find_all("a", class_="obj_galley_link pdf", href=True)]
        return articles