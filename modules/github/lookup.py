from .commit import CommitScraper


class GithubLookup:

    def __init__(self, name: str) -> None:
        self.name = name
        self.stats: dict = {}

    def run(self):
        commit_scraper = CommitScraper(name=self.name)
        self.stats["information"] = commit_scraper.run()
        return self.stats
