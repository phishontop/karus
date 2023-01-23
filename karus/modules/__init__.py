from .roblox.lookup import RobloxLookup
from .minecraft.lookup import MinecraftLookup
from .github.lookup import GithubLookup
from .companyhouse.search import CompanyhouseSearch
from .steam.lookup import SteamLookup
from .discord.lookup import DiscordLookup


lookup_modules = {
    "roblox": {
        "object": RobloxLookup.from_username,
        "kwargs": {"name": None}
    },
    "minecraft": {
        "object": MinecraftLookup,
        "kwargs": {"name": None}
    },
    "github": {
        "object": GithubLookup,
        "kwargs": {"name": None}
    },
    "companyhouse": {
        "object": CompanyhouseSearch,
        "kwargs": {"fullname": None}
    },
    "steam": {
        "object": SteamLookup.from_username,
        "kwargs": {"name": None}
    },
    "discord": {
        "object": DiscordLookup,
        "kwargs": {"discord_id": None}
    }
}


class LookupModuleNotFound(Exception):
    pass


class LookupFactory:

    @staticmethod
    def create_lookup_object(module: str, kwargs: dict):
        lookup_dict = lookup_modules.get(module)
        if lookup_dict is not None:
            lookup_dict["kwargs"] = kwargs
            return lookup_dict["object"](**lookup_dict["kwargs"])

        else:
            raise LookupModuleNotFound(f"{module} is not found")
