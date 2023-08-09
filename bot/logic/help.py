"""This file represents a start logic."""


from aiogram import Router, types
from aiogram.filters import Command

help_router = Router(name='help')


@help_router.message(Command(commands='help'))
async def help_handler(message: types.Message):
    """Help command handler."""
    return await message.answer('Привет! Тут все просто. Нажимай /start и управляй балансом с помощью двух кнопок:\n1. '
                         'Доход\n2. Расход ')