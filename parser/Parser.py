import os
from abc import ABC, abstractmethod
from rich.console import Console
from rich.progress import Progress
from pick import pick
from urllib.request import Request, urlopen
from PyPDF2 import PdfMerger

console = Console()

class Parser(ABC):
    "Abstrak class untuk memparser issue dan link download"

    @abstractmethod
    def getIssue(self):
        pass

    @abstractmethod
    def getLinkDownload(self, link):
        pass

    def selectIssue(self):
        with console.status("[bold green]Get issue...") as status:
            issueLink, issueTexts = self.getIssue()

        selected, index = pick(issueTexts, "Select issue:")
        return (selected, issueLink[index],)

    def downloadAll(self, links, path):
        files = []
        with console.status("[bold green]Downloading...") as status:
            n = 0
            while links:
                article = links.pop(0)
                output_path = os.path.join(path, f"{n}.pdf")
                self.download(article, output_path)
                files.append(output_path)
                n += 1
        return files

    def download(self, url, path):
        # make an HTTP request within a context manager
        with requests.get(url, stream=True) as r:
            
            # check header to get content length, in bytes
            total_length = int(r.headers.get("Content-Length"))

            # implement progress bar with rich
            with Progress(transient=True) as progress:
                progress.add_task("Downloading", total=total_length)

                # save file
                with open(path, "wb") as file:
                    file.write(response.read())

    def merge(self, files, path):
        with console.status("[bold green]Merging...") as status:
            merge = PdfMerger()
            for file in files:
                merge.append(file)
            merge.write(path)
            merge.close()

    def createOutputDirectory(self, issue):
        path = os.path.join("output", self.journal_name, issue)
        if not os.path.exists(path):
            os.makedirs(path, exist_ok=False)
        return path

    def __init__(self, name, url):
        self.journal_name = name
        self.journal_url = url

        try:
            # selected issue
            issue, link = self.selectIssue()
            
            issue = "".join([c for c in issue if c.isalpha() or c.isdigit() or c==' ']).rstrip()

            # create output direcotry
            path = self.createOutputDirectory(issue)

            # get link download list
            with console.status("[bold green]Get fultext link...") as status:
                articles = self.getLinkDownload(link)

            # download files
            files = self.downloadAll(articles, path)

            # merge downloaded files
            self.merge(files, os.path.join(path, f"{issue}.pdf"))

            # done
            console.print(f"Download [red]{name} [yellow i]{issue} [bold green]Done!")
        except Exception as e:
            console.print(f"[red]{e}")
