from typing import TypedDict

from vk_types.vk_api_objects.place import Place


class Geo(TypedDict):
    type: str
    coordinates: str
    place: Place
