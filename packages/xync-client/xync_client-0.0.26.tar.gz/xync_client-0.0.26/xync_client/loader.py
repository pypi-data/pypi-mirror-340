from aiogram import Bot
from dotenv import load_dotenv
from os import getenv as env

load_dotenv()

if not (TOKEN := env("TOKEN")):
    import logging
    from os.path import abspath

    logging.warning(abspath("."))
    load_dotenv("../../../../..")
    logging.warning(abspath("../../../../.."))
    logging.info(TOKEN := env("TOKEN"))

bot: Bot = Bot(token=TOKEN)
PG_DSN = f"postgres://{env('POSTGRES_USER')}:{env('POSTGRES_PASSWORD')}@{env('POSTGRES_HOST', 'xyncdbs')}:{env('POSTGRES_PORT', 5432)}/{env('POSTGRES_DB', env('POSTGRES_USER'))}"
TG_API_ID = env("TG_API_ID")
TG_API_HASH = env("TG_API_HASH")
