from typing import TypedDict

from src.vk_types.vk_api_objects.group import Group


class Response(TypedDict):
    count: int
    items: list[int] | list[Group]
    last_updated_time: int


class GroupsGet(TypedDict):
    """https://dev.vk.com/ru/method/groups.get"""

    response: Response
