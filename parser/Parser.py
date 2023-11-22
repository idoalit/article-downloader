import os
import platform
import inquirer
from abc import ABC, abstractmethod
from rich.console import Console
from rich.progress import (
    BarColumn,
    DownloadColumn,
    Progress,
    TaskID,
    TextColumn,
    TimeRemainingColumn,
    TransferSpeedColumn,
)
from urllib.request import Request, urlopen
from concurrent.futures import ThreadPoolExecutor
import signal
from functools import partial
from threading import Event
from typing import Iterable
from PyPDF2 import PdfMerger

console = Console()

progress = Progress(
    TextColumn("[bold blue]{task.fields[filename]}", justify="right"),
    BarColumn(bar_width=None),
    "[progress.percentage]{task.percentage:>3.1f}%",
    "•",
    DownloadColumn(),
    "•",
    TransferSpeedColumn(),
    "•",
    TimeRemainingColumn(),
    transient=True
)

done_event = Event()

def handle_sigint(signum, frame):
    done_event.set()

signal.signal(signal.SIGINT, handle_sigint)


class Parser(ABC):
    "Abstrak class untuk memparser issue dan link download"

    @abstractmethod
    def getIssue(self):
        pass

    @abstractmethod
    def getLinkDownload(self, link):
        pass

    def selectIssue(self):
        with console.status(f"[yellow]{self.journal_name} [bold green]get issue...") as status:
            issueLink, issueTexts = self.getIssue()

        # add quit option
        issueTexts.append("⛔️ quit")

        questions = [
        inquirer.List('issue', message="Select issue:", choices=issueTexts)
        ]
        answers = inquirer.prompt(questions)

        selected = answers['issue']

        if selected == "⛔️ quit":
            exit()

        index = issueTexts.index(selected)
        return (selected, issueLink[index],)

    def copy_url(self, task_id: TaskID, url: str, path: str) -> None:
        """Copy data from a url to a local file."""
        # progress.console.log(f"Requesting {url}")
        response = urlopen(url)
        # This will break if the response doesn't contain content length
        progress.update(task_id, total=int(response.info()["Content-length"]))
        with open(path, "wb") as dest_file:
            progress.start_task(task_id)
            for data in iter(partial(response.read, 32768), b""):
                dest_file.write(data)
                progress.update(task_id, advance=len(data))
                if done_event.is_set():
                    return
                    
        progress.update(task_id, visible=False)
        # progress.console.log(f"Downloaded {path}")

    def download(self, urls: Iterable[str], dest_dir: str):
        """Download multiple files to the given directory."""
        files = []
        with progress:
            with ThreadPoolExecutor(max_workers=4) as pool:
                for index, url in enumerate(urls):
                    if url is None: continue
                    
                    filename = url.split("/")[-1]
                    dest_path = os.path.join(dest_dir, filename)

                    split_tup = os.path.splitext(dest_path)
                    if split_tup[1] != ".pdf":
                        filename = f"{index}.pdf"
                        dest_path = os.path.join(dest_dir, filename)

                    task_id = progress.add_task(
                        "download", filename=filename, start=False)
                    pool.submit(self.copy_url, task_id, url, dest_path)
                    files.append(dest_path)
        return files

    def merge(self, files, path):
        with console.status("[bold green]Merging...") as status:
            merge = PdfMerger()
            for file in files:
                merge.append(file)
            merge.write(path)
            merge.close()

    def createOutputDirectory(self, issue):
        if platform.system() == 'Windows':
            path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop', 'Journals', self.journal_name, issue)
        else:
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

            issue = "".join([c for c in issue if c.isalpha()
                            or c.isdigit() or c == ' ']).rstrip()

            # create output direcotry
            path = self.createOutputDirectory(issue)

            # get link download list
            with console.status(f"[yellow]{name} [cyan]{issue} [bold green]get fulltext link...") as status:
                articles = self.getLinkDownload(link)

            # download files
            files = self.download(articles, path)

            # merge downloaded files
            self.merge(files, os.path.join(path, f"{issue}.pdf"))

            # done
            console.print(
                f"Download [red]{name} [yellow i]{issue} [bold green]Done!")
            console.print(f"Your files saved to: [green]{path}")
        except Exception as e:
            console.print(f"[red]{e}")
