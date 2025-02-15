from typing import Any, TypedDict

from src.vk_types.vk_api_objects.group import Group
from src.vk_types.vk_api_objects.post import Post
from src.vk_types.vk_api_objects.user import User


class Response(TypedDict):
    count: int
    items: list[Post]
    reaction_sets: list[dict[str, Any]]
    next_from: str
    total_count: int
    profiles: list[User]
    groups: list[Group]


class NewsfeedSearch(TypedDict):
    """https://dev.vk.com/ru/method/newsfeed.search"""

    response: Response
