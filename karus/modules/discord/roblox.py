import requests
from dataclasses import dataclass


@dataclass
class RobloxUser:
    id: int
    username: str
    display_name: str


class RobloxUserFactory:

    @staticmethod
    def create(roblox_id: str) -> RobloxUser:
        data = {"roblox_id": roblox_id}

        response = requests.post(
            url="https://users.roblox.com/v1/users",
            json={"userIds": [roblox_id]}
        )

        user = response.json()[0]
        data["username"] = user["name"]
        data["display_name"] = user["displayName"]

        return RobloxUser(**data)
