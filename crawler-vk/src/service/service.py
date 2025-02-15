import logging
from typing import Any

from src.client.client import Client
from src.db.dal import DAL
from src.service.decorators.rate_limited import rate_limited
from src.vk_types.request.params import (
    GroupsGetByIdParams,
    GroupsGetParams,
    GroupsSearchParams,
    NewsfeedSearchParams,
    UsersGetParams,
    WallGetByIdParams,
    WallGetParams,
)
from src.vk_types.response.groups_get import GroupsGet
from src.vk_types.response.groups_get_by_id import GroupsGetById
from src.vk_types.response.groups_search import GroupsSearch
from src.vk_types.response.newsfeed_search import NewsfeedSearch
from src.vk_types.response.users_get import UsersGet
from src.vk_types.response.wall_get import WallGet
from src.vk_types.response.wall_get_by_id import WallGetById
from src.vk_types.result import APIResponse

log = logging.getLogger(__name__)


class Service:
    """Service layer for interacting with different VK API endpoints."""

    RATE_LIMIT = 5

    def __init__(self, client: Client, dal: DAL) -> None:
        """Initialize the service with a VK API client and database access
        layer."""
        self.client = client
        self.dal = dal

    def _save_request(
        self,
        endpoint: str,
        params: dict[str, Any],
        status_code: int,
    ) -> int:
        """Logs the API request to the database and returns its ID."""
        if "access_token" in params:
            params = params.copy()
            params.pop("access_token")
        request_id = self.dal.save_request(endpoint, params, status_code)
        log.info(f"API request saved to DB with ID={request_id}")
        return request_id

    @rate_limited(RATE_LIMIT)
    def _execute_request(
        self,
        method: str,
        params: dict[str, Any],
        user_token: str | None = None,
    ) -> tuple[int, dict[str, Any]]:
        """Executes a request to the VK API, logs it, and returns the
        response."""
        endpoint = f"/method/{method}"
        log.info(f"Executing request: {endpoint} with params: {params}")
        response = self.client.make_request(endpoint, params, user_token)
        request_id = self._save_request(endpoint, params, response.status_code)
        response = response.json()
        log.info(f"Received response from API request ID={request_id}")
        return request_id, response

    def get_group_by_id(
        self,
        group_id: int,
    ) -> APIResponse[GroupsGetById]:
        """Retrieve information about a group."""
        method = "groups.getById"
        params: GroupsGetByIdParams = {"group_id": str(group_id)}
        return APIResponse[GroupsGetById](
            self._execute_request(method, params),
            lambda x: len(x["response"]["groups"]) == 0
            or x["response"]["groups"][0]["name"] == "",
        )

    def get_groups_by_user(
        self,
        user_id: int,
    ) -> APIResponse[GroupsGet]:
        """Retrieve a list of group ids for the specified user."""
        method = "groups.get"
        params: GroupsGetParams = {"user_id": str(user_id)}
        return APIResponse[GroupsGet](
            self._execute_request(method, params),
            lambda x: x["response"]["count"] == 0,
        )

    def search_groups_by_query(
        self,
        user_token: str,
        query: str,
        count: int = 10,
    ) -> APIResponse[GroupsSearch]:
        """Search for VK groups based on a query."""
        method = "groups.search"
        params: GroupsSearchParams = {"q": query, "count": count}
        return APIResponse[GroupsSearch](
            self._execute_request(method, params, user_token),
            lambda x: x["response"]["count"] == 0,
        )

    def search_posts_by_query(
        self,
        query: str,
        count: int = 10,
    ) -> APIResponse[NewsfeedSearch]:
        """Search for posts containing a specific query."""
        method = "newsfeed.search"
        params: NewsfeedSearchParams = {"q": query, "count": count}
        return APIResponse[NewsfeedSearch](
            self._execute_request(method, params),
            lambda x: x["response"]["count"] == 0,
        )

    def get_users_by_id(
        self,
        user_ids: str | int,
    ) -> APIResponse[UsersGet]:
        """Retrieve a list of users."""
        method = "users.get"
        params: UsersGetParams = {"user_ids": str(user_ids)}
        return APIResponse[UsersGet](
            self._execute_request(method, params),
            lambda x: len(x["response"]) == 0,
        )

    def get_wall_post_by_id(
        self,
        owner_id: int,
        post_id: int,
    ) -> APIResponse[WallGetById]:
        """Fetch a specific post from a VK community or user wall."""
        method = "wall.getById"
        params: WallGetByIdParams = {"posts": f"{owner_id}_{post_id}"}
        return APIResponse[WallGetById](
            self._execute_request(method, params),
            lambda x: len(x["response"]["items"]) == 0,
        )

    def get_wall_posts_by_owner(
        self,
        owner_id: int,
        count: int = 10,
    ) -> APIResponse[WallGet]:
        """Fetch latest posts from a VK group wall."""
        method = "wall.get"
        params: WallGetParams = {"owner_id": owner_id, "count": count}
        return APIResponse[WallGet](
            self._execute_request(method, params),
            lambda x: x["response"]["count"] == 0,
        )
