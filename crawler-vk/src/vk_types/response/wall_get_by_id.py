from typing import TypedDict

from src.vk_types.vk_api_objects.group import Group
from src.vk_types.vk_api_objects.post import Post
from src.vk_types.vk_api_objects.user import User


class Response(TypedDict):
    items: list[Post]  # One element list
    profiles: list[User]
    groups: list[Group]


class WallGetById(TypedDict):
    """https://dev.vk.com/ru/method/wall.getById"""

    response: Response
