from typing import TypedDict

from vk_types.vk_api_objects.group import Group


class Response(TypedDict):
    count: int  # Number of matches.
    items: list[Group]


class GroupsSearch(TypedDict):
    """https://dev.vk.com/ru/method/groups.search"""

    response: Response
