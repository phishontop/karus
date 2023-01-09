from modules import RobloxLookup, MinecraftLookup, GithubLookup


class Username:
    """Represents a Username"""
    def __init__(self, name: str, module: str) -> None:
        self.name = name
        self.module = module
        self.results = {}

    def run(self):
        modules_dict = {
            "roblox": {"lookup": RobloxLookup.from_username},
            "minecraft": {"lookup": MinecraftLookup},
            "github": {"lookup": GithubLookup}
        }

        if self.module == "all":
            for name, module_lookup in modules_dict.items():
                self.results[name] = module_lookup["lookup"](self.name).run()

        else:
            lookup = modules_dict.get(self.module)["lookup"]
            self.results[self.module] = lookup(self.name).run()
