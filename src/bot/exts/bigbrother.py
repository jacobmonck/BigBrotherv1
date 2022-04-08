from disnake.ext.commands import Cog

from src.bot.impl import Bot


class BigBrother(Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot


def setup(bot: Bot) -> None:
    bot.add_cog(BigBrother(bot))
