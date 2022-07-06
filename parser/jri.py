import re
from parser.Parser import Parser
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen


class JRI(Parser):

    def getIssue(self):
        req = Request(self.journal_url, headers={'User-Agent': 'Mozilla/5.0'})
        html_page = urlopen(req).read()
        soup = BeautifulSoup(html_page, 'lxml')
        issues = soup.select('#year a[style="color:#00f"]', href=True)
        issueLink = ["https://www.jri.ir" + e.get("href") for e in issues]
        issueTexts = [re.sub(r"\s+", " ", e.getText()).strip() for e in issues]
        return (issueLink, issueTexts)

    def getLinkDownload(self, url):
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        html_page = urlopen(req).read()
        soup = BeautifulSoup(html_page, 'lxml')
        articles = ["https://www.jri.ir" + a['href'].replace('/article/', '/documents/fullpaper/en/') + ".pdf"
                    for a in soup.find_all("a", class_="list-group-item", href=True)]
        return articles
