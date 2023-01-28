import requests
from dataclasses import dataclass
from PIL import ImageFile


@dataclass
class Viewport:
    name: str
    portraitWidth: int
    landscapeWidth: int


class Image:

    def __init__(self, response) -> None:
        parser = ImageFile.Parser()
        parser.feed(response.content)
        self.width, self.height = parser.image.size


class ImageLookup:

    def __init__(self, image_url: str) -> None:
        self.image_url = image_url
        self._image = None
        self._viewports = None

    @property
    def image(self) -> Image:
        if self._image is None:
            response = requests.get(
                url=self.image_url,
                stream=True,
                headers={"Range": "bytes=0-2000000"}
            )

            self._image = Image(response=response)

        return self._image

    @property
    def viewports(self) -> list:
        if self._viewports is None:
            response = requests.get(
                "https://raw.githubusercontent.com/DevExpress/device-specs/master/viewport-sizes.json")
            response_json = response.json()
            viewport_list = [Viewport(**value) for key, value in response_json.items()]
            viewport_list.append(Viewport(name="Samsung Galaxy S10 Lite", landscapeWidth=2400, portraitWidth=1080))
            viewport_list.append(Viewport(name="Xiaomi Redmi Note 9 Pro", landscapeWidth=2400, portraitWidth=1080))

            self._viewports = viewport_list

        return self._viewports

    def run(self) -> dict:
        devices = [
            viewport.name
            for viewport in self.viewports
            if (viewport.portraitWidth == self.image.width and
                viewport.landscapeWidth == self.image.height)
        ]

        return {
            "image_metadata": {
                "devices": [devices]
            }
        }
