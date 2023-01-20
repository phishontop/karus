import requests
import bs4
from dataclasses import dataclass

from .game import GameFactory
from .review import ReviewFactory


@dataclass
class Profile:
    username: str
    url: str
    id: str


@dataclass
class PreviousName:
    newname: str
    timechanged: str


class SteamSession:
    """Represents an HTTP session with steam"""
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:108.0) Gecko/20100101 Firefox/108.0"})
        self._session_id = None

    @property
    def session_id(self):
        if self._session_id is None:
            self.session.get("https://steamcommunity.com/")
            self._session_id = self.session.cookies["sessionid"]

        return self._session_id

    def user_search(self, username: str):
        response = self.session.get(
            url=f"https://steamcommunity.com/search/SearchCommunityAjax",
            params={
                "text": username,
                "filter": "users",
                "sessionid": self.session_id,
                "steamid_user": "false",
                "page": "1"
            }
        )

        response_json = response.json()
        soup = bs4.BeautifulSoup(
            response_json["html"],
            builder=bs4.builder_registry.lookup(*bs4.BeautifulSoup.DEFAULT_BUILDER_FEATURES)
        )

        return [
            Profile(
                username=element.text,
                id=element["href"].split("/")[4],
                url=element["href"]
            )
            for element in soup.find_all("a", href=True)
            if element.text
        ]


class User:

    def __init__(self, profile: Profile, session: SteamSession):
        self.profile = profile
        self.client = session
        self.profile_soup = bs4.BeautifulSoup(
            self.client.session.get(self.profile.url).text,
            builder=bs4.builder_registry.lookup(*bs4.BeautifulSoup.DEFAULT_BUILDER_FEATURES)
        )

        self.review_soup = bs4.BeautifulSoup(
            self.client.session.get(f"{self.profile.url}/reviews/").text,
            builder=bs4.builder_registry.lookup(*bs4.BeautifulSoup.DEFAULT_BUILDER_FEATURES)
        )

    def get_previous_usernames(self):
        response = self.client.session.post(f"{self.profile.url}/ajaxaliases/", json={})
        response_json = response.json()

        return [
            PreviousName(**change)
            for change in response_json
        ]

    def get_information(self):
        data = {
            "bio": self.profile_soup.find("div", {"class": ["profile_summary", "noexpand"]}).text,
            "location": self.profile_soup.find("div", {"class": ["header_real_name", "ellipsis"]}).text
        }

        for key, value in data.items():
            data[key] = "".join(value.replace("\t", "").splitlines()[-1:])

        return data

    def get_games(self):
        recent_games = self.profile_soup.find_all("div", {"class": "recent_game"})

        return [
            GameFactory.create(game)
            for game in recent_games
        ]

    def get_reviews(self):
        recent_reviews = self.review_soup.find_all("div", {"class": "review_box"})

        return [
            ReviewFactory.create(review)
            for review in recent_reviews
        ]


class SteamLookup:

    def __init__(self, user: User) -> None:
        self.user = user

    @classmethod
    def from_username(cls, name: str):
        session = SteamSession()
        users = session.user_search(username=name)

        for profile in users:
            if profile.username == name or profile.id == name:
                user = User(profile=profile, session=session)
                return cls(user=user)

    def run(self):
        return {
            "steam": {
                "reviews": [review.__dict__ for review in self.user.get_reviews()],
                "games": [game.__dict__ for game in self.user.get_games()]
            }
        }

