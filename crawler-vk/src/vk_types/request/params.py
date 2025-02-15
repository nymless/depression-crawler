from typing import Literal, Required, TypedDict


class GroupsGetByIdParams(TypedDict, total=False):
    """https://dev.vk.com/ru/method/groups.getById"""

    group_ids: str
    group_id: Required[str]
    fields: str


class GroupsGetParams(TypedDict, total=False):
    """https://dev.vk.com/ru/method/groups.get"""

    user_id: Required[str]
    extended: Literal[0, 1]
    filter: Literal[
        "admin",
        "editor",
        "moder",
        "advertiser",
        "groups",
        "publics",
        "events",
        "hasAddress",
    ]
    fields: str
    offset: int
    count: int


class GroupsSearchParams(TypedDict, total=False):
    """https://dev.vk.com/ru/method/groups.search"""

    q: Required[str]
    count: int
    offset: int
    type: Literal["group", "page", "event"]
    country_id: int
    city_id: int
    future: Literal[0, 1]
    market: Literal[0, 1]
    sort: Literal[0, 6]


class NewsfeedSearchParams(TypedDict, total=False):
    """https://dev.vk.com/ru/method/newsfeed.search"""

    q: Required[str]
    count: int
    offset: int
    start_from: str
    latitude: str
    longitude: str
    start_time: int
    end_time: str
    start_id: str
    extended: Literal[0, 1]
    fields: str


class UsersGetParams(TypedDict, total=False):
    """https://dev.vk.com/ru/method/users.get"""

    user_ids: Required[str]
    name_case: Literal["nom", "gen", "dat", "acc", "ins", "abl"]
    from_group_id: int
    fields: str


class WallGetByIdParams(TypedDict, total=False):
    """https://dev.vk.com/ru/method/wall.getById"""

    posts: Required[str]
    extended: Literal[0, 1]
    copy_history_depth: int
    fields: str


class WallGetParams(TypedDict, total=False):
    """https://dev.vk.com/ru/method/wall.get"""

    owner_id: Required[int]
    domain: str
    offset: int
    count: int
    filter: Literal["suggests", "postponed", "owner", "others", "all", "donut"]
    extended: Literal[0, 1]
    fields: str
