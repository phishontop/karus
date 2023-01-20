import requests
import bs4
from threading import Thread
import collections
import re
from dataclasses import dataclass


class CommitScraper:

    def __init__(self, name: str):
        self.name = name
        self.commits_text = []
        self.threads = []
        self.stats = collections.defaultdict(list)

    def get_information(self, url):
        extract = ExtractFactory.create(link=url)
        info = extract.information
        for key, value_list in info.__dict__.items():
            current_values = self.stats[key]
            unique_values = [item for item in value_list if item not in current_values]
            self.stats[key] += unique_values

    def get_commits(self, url: str):
        response = requests.get(url)
        if response.status_code == 404:
            response = requests.get(url.replace("main", "master"))

        soup = bs4.BeautifulSoup(
            response.text,
            builder=bs4.builder_registry.lookup(*bs4.BeautifulSoup.DEFAULT_BUILDER_FEATURES)
        )

        for a in soup.find_all('a', href=True):
            if f"/{self.name}/{self.name}/tree/" in a['href'].lower():
                thread = Thread(target=self.get_information, args=(a['href'],))
                self.threads.append(thread)

            elif f"/{self.name}/{self.name}/commits/main?after=" in a['href']:
                self.get_commits(url=a['href'])

    def run(self):
        InformationListFactory.create()
        self.get_commits(f"https://github.com/{self.name}/{self.name}/commits/main")

        for thread in self.threads:
            thread.start()

        for thread in self.threads:
            thread.join()

        return self.stats


class Singleton(type):
    _modules = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._modules:
            cls._modules[cls] = super().__call__(*args, **kwargs)
        return cls._modules[cls]


@dataclass
class CommitInformation:
    emails: list
    age: list
    coding_languages: list
    ide_list: list
    os_list: list
    discord_tag: list
    discord_id: list
    country: list
    eth_wallet: list


class CommitInformationFactory:

    @staticmethod
    def create(extracted_info: dict) -> CommitInformation:
        new_extracted_info = {}
        for info_name, info_list in extracted_info.items():
            new_extracted_info[info_name] = list(dict.fromkeys(info_list))

        return CommitInformation(**new_extracted_info)


class Extract:

    def __init__(self, raw_text: str) -> None:
        self.information_list = InformationList()

        for word in ['[', ']', '"', "'", ",", "`", "*", "/", ")", "(", "=", "<", ">"]:
            raw_text = raw_text.replace(word, " ")

        self.words: list = [
            word.lower()
            for line in raw_text.splitlines()
            for word in line.split()
            if word not in ["width", "height", "src=", "alt="]
        ]

    @property
    def information(self) -> CommitInformation:
        regex_data = {
            "age": [
                word
                for word in self.words
                if word.isdigit()
                if len(word) == 2 and int(word) > 12
            ],
            "emails": [email for word in self.words for email in re.findall(r'[\w.+-]+@[\w-]+\.[\w.-]+', word)],
            "coding_languages": [
                word
                for word in self.words
                if word in self.information_list.coding_languages and word not in [
                    "dm", "m", "e", "d", "c", "click", "self"
                ]
            ],
            "ide_list": [
                word
                for word in self.words
                if word in ["vscode", "vsc", "pycharm", "visualstudio", "intellij", "eclipse"]
            ],
            "os_list": [
                word
                for word in self.words
                if word in ["windows", "linux", "mac"]
            ],
            "discord_tag": [
                disc_tag
                for word in self.words
                for disc_tag in re.findall(r"^.{3,32}#[0-9]{4}$", word)
            ],
            "discord_id": [
                word
                for word in self.words
                if word.isdigit() and len(word) > 17
            ],
            "country": [
                word
                for word in self.words
                if word.title() in self.information_list.countries
            ],
            "eth_wallet": [
                wallet
                for word in self.words
                for wallet in re.findall(r"\b0x[a-f0-9]{40}\b", word)
            ]
        }

        return CommitInformationFactory.create(extracted_info=regex_data)


class ExtractFactory:

    @staticmethod
    def create(link: str) -> Extract:
        """Factory pattern for creating the Extract object"""
        readme_list = [
            "README.md",
            "README.MD",
            "readme.md",
            "README.md",
            "README.mdx"
        ]

        for file in readme_list:
            link_split = link.split("/")
            name, commit_id = link_split[1], link_split[4]
            response = requests.get(f"https://raw.githubusercontent.com/{name}/{name}/{commit_id}/{file}")
            if response.status_code == 200:
                return Extract(raw_text=response.text)

        return Extract(raw_text="")


@dataclass(frozen=True)
class InformationList(metaclass=Singleton):
    email_domains: list = None
    countries: list = None
    coding_languages: list = None


class InformationListFactory:

    @staticmethod
    def create() -> InformationList:
        data = {}
        urls = {
            "email_domains": "https://gist.githubusercontent.com/ammarshah/f5c2624d767f91a7cbdc4e54db8dd0bf/raw/660fd949eba09c0b86574d9d3aa0f2137161fc7c/all_email_provider_domains.txt",
            "countries": "https://gist.githubusercontent.com/dariusz-wozniak/656f2f9070b4205c5009716f05c94067/raw/b291d58154c85dad840859fef4e63efb163005b0/list-of-countries.txt",
            "coding_languages": "https://raw.githubusercontent.com/csurfer/gitlang/master/languages.txt"
        }

        for name, url in urls.items():
            response = requests.get(url)
            data[name] = response.text.splitlines()

        return InformationList(**data)
