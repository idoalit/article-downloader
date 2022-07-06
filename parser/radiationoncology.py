import re
from parser.Parser import Parser
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen


class RadiationOncology(Parser):

    def getIssue(self):
        req = Request(self.journal_url, headers={'User-Agent': 'Mozilla/5.0'})
        html_page = urlopen(req).read()
        soup = BeautifulSoup(html_page, 'lxml')
        issues = soup.select(
            'ul[data-test="springer-volumes-and-issues"] a', href=True)
        issueLink = ["https://link.springer.com" +
                     e.get("href") for e in issues]
        issueTexts = [re.sub(r"\s+", " ", e.getText()).strip() for e in issues]
        return (issueLink, issueTexts)

    def getLinkDownload(self, url):
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        html_page = urlopen(req).read()
        soup = BeautifulSoup(html_page, 'lxml')
        articles = [a['href'].replace('/article/', '/content/pdf/') + ".pdf"
                    for a in soup.select('ol[data-test="issue-articles"] a', href=True)]
        numbers = [n.getText().replace("Article:").strip()
                   for n in soup.select('li[data-test="article-number"]')]
        return articles
