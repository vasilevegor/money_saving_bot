import os
import asyncio
import logging
from aiogram import Dispatcher, Bot
from aiogram.fsm.storage.memory import MemoryStorage
from sqlalchemy import URL
from dotenv import load_dotenv, dotenv_values

from logic import start_router, balance_router, register_user_commands, help_router

from db import BaseModel, proceed_schemas, get_session_maker, create_async_engine


load_dotenv()


async def main():
    logging.basicConfig(level=logging.DEBUG)

    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)

    dp.include_router(start_router)
    dp.include_router(balance_router)
    dp.include_router(help_router)

    register_user_commands(dp)

    bot = Bot(token=os.getenv('token'), parse_mode='HTML')

    postgres_url = URL.create(
        "postgresql+asyncpg",
        username=os.getenv("db_user"),
        password=os.getenv("db_pass"),
        host="localhost",
        port=os.getenv("db_port"),
        database=os.getenv("db_name")

    )

    async_engine = create_async_engine(postgres_url)
    session_maker = get_session_maker(async_engine)
    # await proceed_schemas(async_engine, BaseModel.metadata)

    await dp.start_polling(bot, session_maker=session_maker)


if __name__ == '__main__':
    asyncio.run(main())
