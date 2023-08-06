from aiogram import Router, types
from aiogram.filters import Command
from sqlalchemy.orm import sessionmaker

from db.money import get_balance
from bot.middlewares.register_check import RegisterCheck

balance_router = Router(name='balance')


@balance_router.message(Command(commands=["balance"]))
async def check_balance(message: types.Message, session_maker: sessionmaker) -> None:
    balance = await get_balance(message.from_user.id, session_maker=session_maker)
    await message.answer(f'Текущий баланс:\n{balance.balance}')

