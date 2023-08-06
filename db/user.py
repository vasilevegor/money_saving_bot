from datetime import datetime, date
import datetime

from sqlalchemy import Column, Integer, VARCHAR, DATE, String, BigInteger
from sqlalchemy.orm import Mapped, mapped_column, sessionmaker

from .base import BaseModel


class User(BaseModel):
    __tablename__ = 'users'

    user_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, unique=True, nullable=False)

    username: Mapped[str] = mapped_column(String(32), unique=False, nullable=True)

    reg_date: Mapped[datetime.datetime] = mapped_column(DATE, default=datetime.date.today())

    upd_date: Mapped[datetime.datetime] = mapped_column(DATE, default=datetime.date.today())

    def __str__(self):
        return f"<User:{self.user_id}>"

    def __repr__(self):
        return self.__str__()
