import requests
import bs4
from threading import Thread
import collections
import re


class CommitScraper:

    def __init__(self, name: str):
        self.name = name
        self.commits_text = []
        self.threads = []
        self.stats = collections.defaultdict(list)

    def get_commit_text(self, url):
        text = CommitTextFactory.create(link=url)
        self.commits_text.append(text)

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
                thread = Thread(target=self.get_commit_text, args=(a['href'],))
                self.threads.append(thread)

            elif f"/{self.name}/{self.name}/commits/main?after=" in a['href']:
                self.get_commits(url=a['href'])

    def run(self):
        self.get_commits(f"https://github.com/{self.name}/{self.name}/commits/main")
        for thread in self.threads:
            thread.start()

        for thread in self.threads:
            thread.join()

        for commit in self.commits_text:
            if commit is not None:
                info = commit.extract_info()
                for name, values in info.items():
                    for value in values:
                        if value not in self.stats[name]:
                            self.stats[name].append(value)

        return self.stats


class CommitText:

    """Represents raw text on the commit"""
    def __init__(self, raw_text: str) -> None:
        self.raw_text = raw_text
        self.emails_list = CommitText.get_emails_list()

    @staticmethod
    def get_emails_list():
        response = requests.get("https://gist.githubusercontent.com/ammarshah/f5c2624d767f91a7cbdc4e54db8dd0bf/raw/660fd949eba09c0b86574d9d3aa0f2137161fc7c/all_email_provider_domains.txt")
        return response.text.splitlines()

    @staticmethod
    def extract_ide(word: str):
        # TODO: add more IDEs
        return word in ["vscode", "vsc", "pycharm", "visualstudio", "intellij", "eclipse"]

    @staticmethod
    def extract_os(word: str):
        return word in ["windows", "linux", "mac", "macos"]

    @staticmethod
    def extract_coding_lang(word: str):
        return word in ["go", "python",
                        "html", "css",
                        "js", "go",
                        "golang", "javascript",
                        "node", "nodejs",
                        "node.js", "c++",
                        "java", "ruby"
                        "c#","csharp",
                        "lua"
                        ]

    def extract_email(self, word: str):
        if "@" in word:
            domain = word.split("@")[1]
            return domain in self.emails_list
        else:
            return False

    @staticmethod
    def extract_discord_tag(word: str):
        word_split = word.split("#")
        if len(word_split) == 2:
            return word_split[1].isdigit()

        else:
            return False

    def check_word(self, word: str):
        # TODO: add bitcoin, eth etc wallet finder
        functions = {
            "email": self.extract_email,
            "age": CommitText.extract_age,
            "skills": CommitText.extract_coding_lang,
            "ide": CommitText.extract_ide,
            "operating_systems": CommitText.extract_os,
            "discord_tag": CommitText.extract_discord_tag,
            "discord_id": CommitText.extract_discord_id,
            "crypto_wallets": CommitText.extract_crypto_address
        }

        for name, func in functions.items():
            if func(word):
                return name

        return ""

    @staticmethod
    def extract_discord_id(word):
        return word.isdigit() and len(word) > 17

    @staticmethod
    def extract_crypto_address(word):
        regex_list = [
            "^(bc1|[13])[a-zA-HJ-NP-Z0-9]{25,39}$",
            "/(0x[a-f0-9]{40})/g;"
        ]
        for item in regex_list:
            if re.search(item, word) is not None:
                return True

        return False

    @staticmethod
    def extract_age(word):
        if word.isdigit():
            return len(word) == 2 and int(word) > 12

        else:
            return False

    @staticmethod
    def clean_word(word: str):
        remove_list = ['[', ']', '"', "'", ",", "`", "*", "/", ")", "(", "=", "<", ">"]
        blacklist = ["width", "height", "src=", "alt="]

        for item in blacklist:
            if item in word:
                return []

        new_words = []
        current_string = ""
        for char in word:
            if char in remove_list:
                new_words.append(current_string)
                current_string = ""

            else:
                current_string += char.lower()

        if current_string:
            new_words.append(current_string)

        print(f"[CLEANED WORD] {word} ---> {new_words}")
        return new_words

    def extract_info(self):
        # TODO: fix indents cuz im stupid
        information = collections.defaultdict(list)
        for line in self.raw_text.splitlines():
            for word in line.split():
                new_words = CommitText.clean_word(word)
                for new_word in new_words:
                    name = self.check_word(new_word)
                    if name:
                        information[name].append(new_word)

        return information


class CommitTextFactory:

    @staticmethod
    def create(link: str) -> CommitText:
        """Factory pattern for creating the CommitText object"""
        ends = ["README.md", "README.MD", "readme.md", "README.md", "README.mdx"]
        for end in ends:
            link_split = link.split("/")
            name, commit_id = link_split[1], link_split[4]
            response = requests.get(f"https://raw.githubusercontent.com/{name}/{name}/{commit_id}/{end}")
            if response.status_code == 200:
                return CommitText(raw_text=response.text)
