from dataclasses import dataclass


@dataclass
class Game:
    name: str
    last_played: str
    time_played: str
    link: str


class GameFactory:

    @staticmethod
    def create(game_element) -> Game:
        stats_element = game_element.find("div", {"class": "game_info_details"})
        stats_text = stats_element.text.replace("\t", "").splitlines()

        game_data = {
            "name": game_element.find("div", {"class": "game_name"}).text,
            "time_played": stats_text[1].replace(" on record", ""),
            "last_played": stats_text[2].replace("last played on ", ""),
            "link": [
                link["href"]
                for link in game_element.find_all("a", href=True)
                if link["href"].startswith("https://steamcommunity.com/app/")
            ][0]
        }

        return Game(**game_data)
