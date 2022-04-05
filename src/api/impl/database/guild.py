from ormar import JSON, Integer, Model

from . import database, metadata


class Guild(Model):
    class Meta:
        tablename = "guilds"
        metadata = metadata
        database = database

    id: int = Integer(primary_key=True)
    data: dict = JSON()
