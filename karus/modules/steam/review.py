from dataclasses import dataclass


@dataclass
class Review:
    time_played: str
    description: str
    game_link: str


class ReviewFactory:

    @staticmethod
    def create(review) -> Review:
        review_element = review.find("div", {"class": "rightcol"})
        time_element = review_element.find("div", {"class": "hours"})
        time_text = time_element.text.replace("\t", "").splitlines()

        data = {
            "time_played": time_text[1].split(" on record")[0],
            "description": review_element.find("div", {"class": ["content"]}).text.replace("\t", ""),
            "game_link": [
                link["href"]
                for link in review.find_all("a", href=True)
                if link["href"].startswith("https://steamcommunity.com/app/")
            ][0]
        }

        return Review(**data)
