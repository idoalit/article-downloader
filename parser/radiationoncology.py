import re
from parser.Parser import Parser
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen


class RadiationOncology(Parser):

    _articles = {}

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
        self.getLinkPerPage(url)
        return [self._articles[i] for i in sorted(self._articles.keys())]

    def getLinkPerPage(self, url):
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        html_page = urlopen(req).read()
        soup = BeautifulSoup(html_page, 'lxml')

        for el in soup.find_all("li", class_="c-list-group__item"):
            link = el.select_one('.c-card__title a').get('href').replace('/article/', '/content/pdf/') + ".pdf"
            number = el.select_one('li[data-test="article-number"]').getText().replace("Article:", "").strip()
            publish = el.select_one('li[data-test="published-on"]').getText().replace("Published:", "").strip()
            self._articles[int(number)] = link

        next_page = soup.select_one('a[data-test="next-page"]')
        if next_page:
            self.getLinkPerPage("https://link.springer.com" + next_page.get('href'))
