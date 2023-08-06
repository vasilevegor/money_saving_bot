from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from sqlalchemy.orm import sessionmaker

from bot.middlewares.register_check import RegisterCheck
from bot.structures import MoneyStates
from db.money import get_balance, set_balance

start_router = Router(name='start')
start_router.message.middleware(RegisterCheck())


@start_router.message(Command(commands=["start"]))
async def start_handler(message: types.Message, session_maker: sessionmaker) -> None:
    """Start command handler."""
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='Доход', callback_data='income'),
                InlineKeyboardButton(text='Расход', callback_data='expense')
            ]
        ])

    await message.answer('Привет! Тут все просто. В сообщении ниже твой актуальный баланс и две кнопки:\n1. '
                         'Доход\n2. Расход ')
    balance = await get_balance(message.from_user.id, session_maker=session_maker)
    await message.answer(f"Баланс: {balance.balance}",
                         reply_markup=markup)


@start_router.callback_query(F.data == 'income')
async def call_income_message(call: types.CallbackQuery, state: FSMContext):
    await state.set_state(MoneyStates.waiting_for_increase)
    cancel_board = ReplyKeyboardBuilder()
    cancel_board.button(text='Отмена')
    await call.message.answer('Введите сумму: ',
                              reply_markup=cancel_board.as_markup(resize_keyboard=True))


@start_router.message(MoneyStates.waiting_for_increase)
async def increase_money(message: types.Message, state: FSMContext, session_maker: sessionmaker):
    if message.text == 'Отмена':
        await state.clear()
        return await start_handler(message, session_maker)

    try:
        value = float(message.text)
    except:
        return message.answer(f'Ошибка. Введите число, для указания копеек используйте "." вместо ","')

    await set_balance(message.from_user.id, value, 0.0, session_maker)
    await state.clear()
    return await start_handler(message, session_maker)


@start_router.callback_query(F.data == 'expense')
async def call_income_message(call: types.CallbackQuery, state: FSMContext):
    await state.set_state(MoneyStates.waiting_for_decrease)
    cancel_board = ReplyKeyboardBuilder()
    cancel_board.button(text='Отмена')
    await call.message.answer('Введите сумму: ',
                              reply_markup=cancel_board.as_markup(resize_keyboard=True))


@start_router.message(MoneyStates.waiting_for_decrease)
async def increase_money(message: types.Message, state: FSMContext, session_maker: sessionmaker):
    if message.text == 'Отмена':
        await state.clear()
        return await start_handler(message, session_maker)

    try:
        value = message.text
        if '-' not in value:
            value = '-' + value
            value = float(value)
    except ValueError:
        return await message.answer('Ошибка. Введите число без пробелов и для отделения целой части используйте "."')

    await set_balance(message.from_user.id, 0.0, value, session_maker)
    await state.clear()
    return await start_handler(message, session_maker)
