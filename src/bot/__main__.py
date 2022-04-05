from dotenv import load_dotenv

from . import Bot

load_dotenv()


def main() -> None:
    bot = Bot()

    for ext in []:
        bot.load_extension(ext)

    bot.run()


if __name__ == "__main__":
    main()
