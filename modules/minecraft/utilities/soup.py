import bs4


class Soup:

    @staticmethod
    def create(html: str) -> bs4.BeautifulSoup:
        return bs4.BeautifulSoup(
            html,
            builder=bs4.builder_registry.lookup(*bs4.BeautifulSoup.DEFAULT_BUILDER_FEATURES)
        )
