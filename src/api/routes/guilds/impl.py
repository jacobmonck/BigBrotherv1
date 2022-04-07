from asyncpg import UniqueViolationError
from fastapi import APIRouter, Request, Response
from loguru import logger
from orjson import dumps, loads
from ormar.exceptions import NoMatch

from src.api.impl.database import Guild

router = APIRouter(prefix="/guilds")


@router.get("/{guild_id}", response_model=Guild)
async def get_guild(request: Request, guild_id: int) -> Guild | Response:
    """
    Get a guild from the API.

    This will attempt to fetch the guild from Redis if it misses it will fetch it from the database and repopulate the cache.
    """

    if cached_guild := await request.app.state.redis.get(guild_id):
        cached_guild = loads(cached_guild)

        guild = {"id": guild_id, "data": cached_guild}

        return Guild(**guild)

    try:
        guild = await Guild.objects.get(id=guild_id)
    except NoMatch:
        return Response("Not Found", status_code=404)

    return guild


@router.post("/{guild_id}", response_model=Guild)
async def update_guild(request: Request, guild_id: int, guild: Guild) -> Guild:
    """
    Update a guild's config.

    This will attempt to update the guild in the database if that fails it will create an entry for the guild in the database.
    """

    # Shitty upsert because Ormar's built in one doesn't work.
    try:
        await guild.save()
    except UniqueViolationError:
        await guild.update()

    await request.app.state.redis.set(guild_id, dumps(guild.data))

    return guild


@router.delete("/{guild_id}", response_model=Guild)
async def delete_guild(request: Request, guild_id: int) -> Response | Guild:

    try:
        guild = await Guild.objects.get(id=guild_id)
    except NoMatch:
        return Response("Not Found", status_code=404)

    await guild.delete()
    await request.app.state.redis.delete(guild_id)

    return guild
