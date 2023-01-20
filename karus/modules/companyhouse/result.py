from dataclasses import dataclass


@dataclass
class Result:
    birthdate: str
    full_name: str
    address: str


class ResultFactory:

    @staticmethod
    def create(officer) -> Result:
        birthdate = officer.find("p", {"class": "meta crumbtrail"}).text.split(" - ")
        if len(birthdate) == 2:
            data = {
                "birthdate": birthdate[1].replace("Born ", ""),
                "full_name":  officer.find("h3").text.lower(),
                "address": officer.find_all("p")[1].text
            }

            return Result(**data)
