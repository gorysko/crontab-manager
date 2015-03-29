"""Cron model."""
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String

from . import Base

class Cron(Base):
    __tablename__ = 'cron'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    status = Column(Integer, nullable=False)
