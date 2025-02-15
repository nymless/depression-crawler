from typing import TypedDict

from src.vk_types.vk_api_objects.user import User


class UsersGet(TypedDict):
    """https://dev.vk.com/ru/method/users.get"""

    response: list[User]
