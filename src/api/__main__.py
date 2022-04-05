from dotenv import load_dotenv
from fastapi import FastAPI

from .impl.database import database

load_dotenv()


app = FastAPI()
app.state.database = database


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
