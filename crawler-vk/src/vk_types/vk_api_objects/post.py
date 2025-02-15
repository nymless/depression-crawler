from typing import Any, Literal, TypedDict

from src.vk_types.vk_api_objects.comments import Comments
from src.vk_types.vk_api_objects.copyright import Copyright
from src.vk_types.vk_api_objects.donut import Donut
from src.vk_types.vk_api_objects.geo import Geo
from src.vk_types.vk_api_objects.likes import Likes
from src.vk_types.vk_api_objects.post_source import PostSource
from src.vk_types.vk_api_objects.reposts import Reposts
from src.vk_types.vk_api_objects.views import Views


class Post(TypedDict):
    """https://dev.vk.com/ru/reference/objects/post"""

    id: int
    owner_id: int
    from_id: int
    created_by: int
    date: int
    text: str
    reply_owner_id: int
    reply_post_id: int
    friends_only: int
    comments: Comments
    copyright: Copyright
    likes: Likes
    reposts: Reposts
    views: Views
    post_type: Literal["post", "copy", "reply", "postpone", "suggest"]
    post_source: PostSource
    attachments: list[dict[str, Any]]
    geo: Geo
    signer_id: int
    copy_history: list[dict[str, Any]]
    can_pin: Literal[0, 1]
    can_delete: Literal[0, 1]
    can_edit: Literal[0, 1]
    is_pinned: int
    marked_as_ads: Literal[0, 1]
    is_favorite: bool
    donut: Donut
    postponed_id: int
