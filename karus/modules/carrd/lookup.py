import bs4
import requests


class CarrdLookup:

    def __init__(self, name: str) -> None:
        self.profile_soup = bs4.BeautifulSoup(
            requests.get(f"https://{name}.carrd.co").text,
            builder=bs4.builder_registry.lookup(*bs4.BeautifulSoup.DEFAULT_BUILDER_FEATURES)
        )

        self.links = [
            link["href"].replace("https://", "")
            for link in self.profile_soup.find_all("a", href=True)
            if link["href"].startswith("https") and "carrd.co" not in link["href"]
        ]

    def run(self):
        return {"carrd": {"links": self.links}}

#p1xiy
