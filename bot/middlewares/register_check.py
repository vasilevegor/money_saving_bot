from typing import Callable, Dict, Any, Awaitable, Union

from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from sqlalchemy import select
from sqlalchemy.engine import ScalarResult
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from db import Money, User

# from db import User, Money


class RegisterCheck(BaseMiddleware):

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Union[Message, CallbackQuery],
        data: Dict[str, Any]
    ) -> Any:
        session_maker = data['session_maker']
        async with session_maker() as session:
            async with session.begin():
                user_result = await session.execute(select(User).where(User.user_id == event.from_user.id))
                money_result = await session.execute(select(Money).where(Money.user_id == event.from_user.id))

                user: User = user_result.one_or_none()
                money: Money = money_result.first()

                if user is not None:
                    pass

                user = User(
                    user_id=event.from_user.id,
                    username=event.from_user.username
                )

                await session.merge(user)

                if money is not None:
                    pass
                else:
                    money = Money(
                        user_id=event.from_user.id,
                        balance=0.0,
                        income=0.0,
                        expense=0.0
                    )
                    await session.merge(money)

        return await handler(event, data)
