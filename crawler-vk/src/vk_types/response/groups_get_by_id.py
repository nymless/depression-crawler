from typing import TypedDict

from vk_types.vk_api_objects.group import Group


class Response(TypedDict):
    groups: list[Group]


class GroupsGetById(TypedDict):
    """https://dev.vk.com/ru/method/groups.getById"""

    response: Response
