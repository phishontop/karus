import requests


class PreviousNameScraper:

    def __init__(self, user_id: int) -> None:
        self.user_id = user_id

    def get_names(self) -> list:
        response = requests.get(f"https://users.roblox.com/v1/users/{self.user_id}/username-history?limit=100&sortOrder=Desc")
        data = response.json().get("data")
        if data is not None:
            return [info["name"] for info in data]

        else:
            return []
