"""This package is used for a bot logic implementation."""
from aiogram import Router, F

from .help import help_router
from .start import start_router
from .balance import balance_router
from handlers import increase

routers = (start_router, help_router, balance_router)


def register_user_commands(router: Router) -> None:
    #router.callback_query.register(increase, F.data == "income")
    pass

