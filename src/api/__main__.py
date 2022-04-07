from os import environ

from aioredis import from_url
from dotenv import load_dotenv
from fastapi import FastAPI

from .impl.database import database
from .routes import guilds_router

load_dotenv()


app = FastAPI(
    title="BigBrother Internal API",
    description="This API is used for the BigBrother Discord Bot to connect the internal services together.",
    prefix="/v1",
)
app.include_router(guilds_router)


app.state.database = database

redis = from_url(environ["REDIS_URI"])
app.state.redis = redis


@app.on_event("startup")
async def startup() -> None:
    database_ = app.state.database

    if not database_.is_connected:
        await database_.connect()


@app.on_event("shutdown")
async def shutdown() -> None:
    database_ = app.state.database

    if database_.is_connected:
        await database_.disconnect()
