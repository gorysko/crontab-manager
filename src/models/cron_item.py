"""Cron item model"""
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship

from . import Base

from cron import Cron

class CronItem(Base):
    __tablename__ = 'cron_item'
    id = Column(Integer, primary_key=True)
    schedule = Column(String, nullable=False)
    command = Column(String, nullable=False)
    status = Column(Integer, nullable=False)
    cron_id = Column(Integer, ForeignKey('cron.id'))
    cron = relationship(Cron)
