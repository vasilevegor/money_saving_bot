"""Data Structures.

This file contains TypedDict structure to store data which will
transfer throw Dispatcher->Middlewares->Handlers.
"""

from typing import TypedDict

from aiogram import Bot
from sqlalchemy.ext.asyncio import AsyncEngine

from bot.structures.role import Role
from db.database import Database


class TransferData(TypedDict):
    """Common transfer data."""

    engine: AsyncEngine
    db: Database
    bot: Bot
    role: Role