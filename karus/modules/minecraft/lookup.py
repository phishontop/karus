import time
from .plancke import PlanckeScraper
from .server import Servers


class MinecraftLookup:

    def __init__(self, name: str):
        self.name = name
        self.stats = {}

    def run(self):
        plancke = PlanckeScraper(name=self.name)

        servers = Servers(name=self.name)
        servers.lookup()

        self.stats["hypixel"] = plancke.get_info()
        self.stats["punishments"] = servers.punishments
        self.stats["purchases"] = servers.purchases

        return {"minecraft": self.stats}
