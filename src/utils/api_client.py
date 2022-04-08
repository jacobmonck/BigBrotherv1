from os import environ
from typing import Optional

from aiohttp import ClientSession
from orjson import dumps


class APIClient:
    def __init__(self) -> None:
        self._api_url = environ["API_BASE_URL"]
        self.__session: ClientSession | None = None

    @property
    def _session(self) -> ClientSession:
        if self.__session is None or self.__session.closed:
            self.__session = ClientSession(
                headers={
                    "Authorization": environ["API_TOKEN"],
                },
                raise_for_status=True,
            )

        return self.__session

    async def _request(self, method: str, route: str, **kwargs) -> dict:
        async with self._session.request(method, self._api_url + route, **kwargs) as response:
            data = await response.json()

            return data

    async def get_guild(self, guild_id: int) -> dict:
        return await self._request("GET", f"/guilds/{guild_id}")

    async def update_guild(self, guild_id: int, data: dict) -> dict:
        return await self._request("POST", f"/guilds/{guild_id}", json=data)

    async def delete_guild(self, guild_id: int) -> dict:
        return await self._request("DELETE", f"/guilds/{guild_id}")
