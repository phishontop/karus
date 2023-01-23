from .roblox import BloxlinkUserFactory
import json


class DiscordLookup:

    def __init__(self, discord_id: str):
        self.api_key = json.load(open("config.json"))["discord"]["bloxlink_api_key"]
        self.discord_id = discord_id

    def run(self):
        data = {}
        if self.api_key is not None:
            data = {"bloxlink": BloxlinkUserFactory.create(discord_id=self.discord_id, api_key=self.api_key)}

        return {"discord": data}
