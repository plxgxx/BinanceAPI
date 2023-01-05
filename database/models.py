from sqlalchemy import Column, ForeignKey, MetaData
from sqlalchemy import BigInteger, Integer, String, Boolean, DateTime, Date, Float

from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

import datetime
from typing import Any
import pytz
from enum import Enum

meta = MetaData(  # automatically name constraints to simplify migrations
    naming_convention={
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }
)
# Any saves from mypy checks of a dynamic class
Base: Any = declarative_base(metadata=meta)


def local_time() -> datetime.datetime:
    """ time in Ukraine """
    kiev_tz = pytz.timezone("Europe/Kiev")
    current_time = datetime.datetime.now(tz=kiev_tz)
    return current_time

class User(Base):
    __tablename__ = "user"

    chat_id = Column(BigInteger, primary_key=True)
    is_banned = Column(Boolean, default=False, nullable=False)
    username = Column(String(35))  # Telegram allows username no longer then 32
    first_name = Column(String)  # first name is unlimited
    last_name = Column(String)
    language = Column(String)
    time_registered = Column(DateTime(timezone=True), default=local_time)
    is_admin = Column(Boolean, default=False, nullable=False)

    def __repr__(self):
        return "<User(chat_id='{}', username='{}', is_banned='{}')>".format(
            self.chat_id, self.username, self.is_banned
        )


class Admin(Base):
    __tablename__ = "admin"

    chat_id = Column(BigInteger, ForeignKey("user.chat_id"), primary_key=True)
    role = Column(String)  # superadmin, sales

    user = relationship("User", backref="admin", foreign_keys=[chat_id])

    def __repr__(self):
        return "<Admin(chat_id='{}')>".format(
            self.chat_id
        )


class NotificationCumfig(Base):
    __tablename__ = "notification_cumfig"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.chat_id"))
    name = Column(String(35))
    currency = Column(String(10))
    payment_choices = Column(String)
    sale_volume = Column(Integer)
    buy_volume = Column(Integer)
    spread_percent = Column(Float)
    completed_orders_percent = Column(Float)
    deals_performed = Column(Integer)
    is_alert = Column(Boolean)
    added_at = Column(Date)

    user = relationship("User", backref="config_rel_user", foreign_keys=[user_id])

    def __repr__(self):
        return "<UserStat(id='{}', user_id='{}', name='{}', added_at='{}')>".format(
            self.id, self.user_id, self.name, self.added_at
        )


