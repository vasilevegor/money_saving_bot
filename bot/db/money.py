from datetime import datetime, date
import datetime

from sqlalchemy import Column, Integer, VARCHAR, DATE, String, BigInteger, ForeignKey, Float
from sqlalchemy import select
from sqlalchemy.orm import Mapped, mapped_column, sessionmaker

from .base import BaseModel


class Money(BaseModel):

    __tablename__ = 'money'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, unique=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"), unique=False)

    balance: Mapped[float] = mapped_column(Float, nullable=False, default=0, unique=False)

    income: Mapped[float] = mapped_column(Float, nullable=True, unique=False)

    expense: Mapped[float] = mapped_column(Float, nullable=True, unique=False)

    def __str__(self):
        return f"<User:{self.user_id}, Balance:{self.balance}"


async def get_balance(user_id: int, session_maker: sessionmaker):
    async with session_maker() as session:
        async with session.begin():
            result = await session.execute(select(Money.balance)
                                           .where(Money.user_id == user_id)
                                           .order_by(Money.id.desc()))
            return result.first()


async def set_balance(user_id: int, income: float, expense: float, session_maker: sessionmaker):
    income = float(income)
    expense = float(expense)
    balance = await get_balance(user_id, session_maker)
    new_balance = balance[0] + (income + expense)
    async with session_maker() as session:
        async with session.begin():
            money = Money(user_id=user_id,
                          balance=new_balance,
                          income=income,
                          expense=expense
                          )
            session.add(money)

