from aiogram.fsm.state import StatesGroup, State


class MoneyStates(StatesGroup):
    balance_state = State()
    waiting_for_increase = State()
    waiting_for_decrease = State()


