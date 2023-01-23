import requests
import bs4

from .result import ResultFactory


class CompanyhouseSearch:

    def __init__(self, fullname: str) -> None:
        self.fullname = fullname.lower()

    @property
    def results(self):
        response = requests.get(f"https://find-and-update.company-information.service.gov.uk/search/officers?q={self.fullname}")

        soup = bs4.BeautifulSoup(
            response.text,
            builder=bs4.builder_registry.lookup(*bs4.BeautifulSoup.DEFAULT_BUILDER_FEATURES)
        )

        officers = soup.find_all("li", {"class": "type-officer"})
        result_list = [ResultFactory.create(officer) for officer in officers]
        return [
            result
            for result in result_list
            if result is not None
            if "full_name" in result.__dict__
            if result.full_name.lower() == self.fullname
        ]

    def run(self) -> dict:
        results = self.results
        if results:
            result = results[0]
            result.address = "".join(result.address.split(",")[:2])
            return {"companyhouse": result.__dict__}

        else:
            return {"companyhouse": {}}
