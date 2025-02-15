from typing import TypedDict

from vk_types.vk_api_objects.group import Group
from vk_types.vk_api_objects.post import Post
from vk_types.vk_api_objects.user import User


class Response(TypedDict):
    count: int
    items: list[Post]
    profiles: list[User]
    groups: list[Group]


class WallGet(TypedDict):
    """https://dev.vk.com/ru/method/wall.get"""

    response: Response
