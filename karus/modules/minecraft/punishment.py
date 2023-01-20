

class Punishment:
    
    def __init__(self, data: list) -> None:
        moderator = 1
        self.moderator = None
        self.type = data[0].text
        self.player = data[1].text

        if len(data) == 6:
            self.moderator = data[2].text
            moderator = 0

        self.reason = data[3-moderator].text
        self.date = data[4-moderator].text

    def as_dict(self) -> dict:
        return {
            "moderator": self.moderator,
            "type": self.type,
            "player": self.player,
            "reason": self.reason,
            "date": self.date
        }


class PunishmentFactory:

    @staticmethod
    def create(soup) -> list:
        punishments = []
        table = soup.find_all("tr")
        for element in table[1:]:
            punishments.append(
                Punishment(element.find_all("td"))
            )
            
        return punishments
