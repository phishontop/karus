import requests
from .utilities.soup import Soup


class PlanckeScraper:

    def __init__(self, name: str) -> None:
        self.name = name
        self.headers = {"User-Agent": "Mozilla/5.0 (X11; CrOS armv7l 13597.84.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.105 Safari/537.36"}
        self.ranks = ["vip", "vip+", "mvp", "mvp+", "mvp++"]

    def get_ranks(self, elements: list):
        for element in elements:
            for rank in self.ranks:
                element_lower = element.text.lower()
                if rank in element_lower:
                    return PlanckeScraper.parse_ranks(element)

    @staticmethod
    def parse_ranks(ranks_soup):
        ranks = []
        for rank in ranks_soup.find_all("li"):
            rank_info = rank.text.split(" - ")

            ranks.append({
                "rank_name": rank_info[0],
                "time": rank_info[1]
            })

        return ranks

    def get_info(self):
        info = {}
        response = requests.get(f"https://plancke.io/hypixel/player/stats/{self.name}", headers=self.headers)

        soup = Soup.create(response.text)

        rank_history = soup.find_all("ul", {"class": "list-unstyled"})
        ranks = self.get_ranks(rank_history)
        info["ranks"] = ranks

        return info
