from os import environ

from aioredis import from_url
from disnake import Intents
from disnake.ext.commands import AutoShardedBot
from loguru import logger

from src.utils import APIClient

intents = Intents.none()
intents.guilds = True
intents.guild_messages = True
intents.webhooks = True


class Bot(AutoShardedBot):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(command_prefix=environ["BOT_PREFIX"], intents=intents, *args, **kwargs)

        self.redis = from_url(environ["REDIS_URI"])

        self.api = APIClient()

    @staticmethod
    async def on_shard_connect(shard_id: int) -> None:
        logger.info(f"Shard {shard_id} is connected.")

    async def on_ready(self) -> None:
        logger.info(
            f"All {self.shard_count or 0} shard(s) are ready this instance can see {len(self.guilds)} guild(s)."
        )

    def load_extension(self, name: str) -> None:
        super().load_extension(name)

        logger.info(f"Loaded extension {name}.")

    def run(self) -> None:
        logger.info("Starting bot...")

        super().run(environ["BOT_TOKEN"])
