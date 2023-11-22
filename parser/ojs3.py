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
        # try another selector
        if not issues:
            issues = soup.find_all("a", class_="cover", href=True)
        issueLink = [e['href'] for e in issues]
        series = soup.find_all("h2", class_="issue_title")
        issueTexts = [re.sub(r"\s+", " ", e.getText()).strip() for e in series]
        return (issueLink, issueTexts)

    def getLinkDownload(self, url):
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        html_page = urlopen(req).read()
        soup = BeautifulSoup(html_page, 'lxml')
        articles = [a['href'].replace('/view/', '/download/')
                    for a in soup.find_all("a", class_="obj_galley_link pdf", href=True)]
        if not articles:
            articles = [self.getInOtherPage(a['href']) for a in soup.select('div[class="art_title linkable"] a', href=True)]
        return articles

    def getInOtherPage(self, url):
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        html_page = urlopen(req).read()
        soup = BeautifulSoup(html_page, 'lxml')
        linkEl = soup.find_all('a', class_="show-pdf", href=True)
        link = None
        if linkEl:
            link = linkEl[0]['href']
            link = re.sub(r"article/view", r"article/download", link)
        return link