import re
import cloudscraper
from pick import pick
from parser.Parser import Parser
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from datetime import date
from rich.console import Console
from cloudscraper import CloudflareIUAMError

console = Console()
MAX_CLOUDFLARE_ATTEMPTS = 10
CLOUDFLARE_WAIT_TIME = 2

class ADM(Parser):

    def selectIssue(self):
        self.year = self.selectYear()

        with console.status(f"[yellow]{self.journal_name} [bold green]get issue...") as status:
            issueLink, issueTexts = self.getIssue()

        selected, index = pick(issueTexts, "Select issue:")
        return (selected, issueLink[index],) 

    def getIssue(self):
        try:
            self._reset_cloudscraper()
            html_page = self.scraper.get(f"{self.journal_url}/year/{str(self.year)}").text
            console.log(html_page)
            return
            soup = BeautifulSoup(html_page, 'lxml')
            issues = soup.find_all("a", class_="visitable", href=True)
            issueLink = [e.get('href') for e in issues]
            issueTexts = [re.sub(r"\s+", " ", e.getText()).strip() for e in issues]
            return (issueLink, issueTexts)
        except CloudflareIUAMError as e:
            print(e)
            print("Retrying...")
            for index in range(1, MAX_CLOUDFLARE_ATTEMPTS + 1):
                print(f"Attempt {index}/{MAX_CLOUDFLARE_ATTEMPTS}... ", end="")
                time.sleep(CLOUDFLARE_WAIT_TIME)
                self._reset_cloudscraper()
                try:
                    self._attempt_daily_blinks_download(languages, base_path)
                    break
                except CloudflareIUAMError:
                    print("FAILED")

    def _reset_cloudscraper(self):
        self.scraper = cloudscraper.create_scraper(delay=10, browser='chrome')

    def getLinkDownload(self, url):
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        html_page = urlopen(req).read()
        soup = BeautifulSoup(html_page, 'lxml')
        articles = [a['href'].replace('/epdf/', '/pdfdirect/') + "?download=true"
                    for a in soup.select(".PdfLink a", href=True)]
        return articles

    def selectYear(self):
        current_year = date.today().year
        year, index = pick(range(2014, int(current_year)+1), "Select the year:")
        return year
