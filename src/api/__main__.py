from os import environ

from hmac import compare_digest
from aioredis import from_url
from dotenv import load_dotenv
from fastapi import FastAPI, Response, Request

load_dotenv()

from .impl.database import database
from .routes import guilds_router

API_TOKEN = environ["API_TOKEN"]

if not API_TOKEN:
    raise Exception("API key not set")

app = FastAPI(
    title="BigBrother Internal API",
    description="This API is used for the BigBrother Discord Bot to connect the internal services together.",
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


@app.middleware("http")
async def check_authentication(request: Request, call_next) -> Response:
    path = request.url.path

    if path.startswith(("/openapi.json", "/docs")):
        return await call_next(request)

    auth = request.headers.get("Authorization")

    if not (auth and compare_digest(auth, API_TOKEN)):
        return Response(status_code=401)

    return await call_next(request)
