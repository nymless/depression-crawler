from typing import TypedDict

from src.vk_types.vk_api_objects.group import Group
from src.vk_types.vk_api_objects.post import Post
from src.vk_types.vk_api_objects.user import User


class Response(TypedDict):
    count: int
    items: list[Post]
    profiles: list[User]
    groups: list[Group]


class WallGet(TypedDict):
    """https://dev.vk.com/ru/method/wall.get"""

    response: Response
