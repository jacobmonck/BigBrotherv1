from ormar import JSON, BigInteger, Model

from . import database, metadata


class Guild(Model):
    class Meta:
        tablename = "guilds"
        metadata = metadata
        database = database

    id: int = BigInteger(primary_key=True)
    data: dict = JSON()
