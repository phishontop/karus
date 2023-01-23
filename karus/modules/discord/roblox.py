import requests
from dataclasses import dataclass


@dataclass
class RobloxUser:
    id: int
    name: str


@dataclass
class BloxlinkUser:
    roblox: RobloxUser
    discord_id: str


class RobloxUserFactory:

    @staticmethod
    def create(roblox_id: str) -> RobloxUser:
        response = requests.get(url=f"https://users.roblox.com/v1/users/{roblox_id}")
        response_json = response.json()

        data = {
            "id": response_json["id"],
            "name": response_json["name"]
        }

        return RobloxUser(**data)


class BloxlinkUserFactory:

    @staticmethod
    def create(discord_id: str, api_key: str):
        response = requests.get(
            url=f"https://v3.blox.link/developer/discord/{discord_id}",
            headers={"api-key": api_key}
        )

        response_json = response.json()
        if response_json["success"]:
            return BloxlinkUser(
                roblox=RobloxUserFactory.create(roblox_id=response_json["user"]["robloxId"]),
                discord_id=discord_id
            )

        else:
            return {}
