from .roblox.lookup import RobloxLookup
from .minecraft.lookup import MinecraftLookup
from .github.lookup import GithubLookup
from .companyhouse.search import CompanyhouseSearch
from .steam.lookup import SteamLookup
from .discord.lookup import DiscordLookup
from .carrd.lookup import CarrdLookup
from .viewport.lookup import ImageLookup


lookup_modules = {
    "roblox": RobloxLookup.from_username,
    "minecraft": MinecraftLookup,
    "github": GithubLookup,
    "companyhouse": CompanyhouseSearch,
    "steam": SteamLookup.from_username,
    "discord": DiscordLookup,
    "carrd": CarrdLookup,
    "viewport": ImageLookup
}


class LookupModuleNotFound(Exception):
    pass


class LookupFactory:

    @staticmethod
    def create_lookup_object(module: str, kwargs: dict):
        lookup = lookup_modules.get(module)
        if lookup is not None:
            return lookup(**kwargs)

        else:
            raise LookupModuleNotFound(f"{module} is not found")
