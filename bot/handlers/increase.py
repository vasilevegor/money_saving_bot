from aiogram import types
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from sqlalchemy.orm import sessionmaker

from bot.db import User, Money
from bot.db.money import set_balance


async def increase(call: types.CallbackQuery, callback_data: CallbackData, session_maker: sessionmaker, state: FSMContext):
    if callback_data == "income":
        await set_balance(call.from_user.id, 10.0, 0.0, session_maker)
    await state.clear()
