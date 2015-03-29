"""Cron item model"""
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from . import Base


class Cron(Base):
    """Cron model."""
    __tablename__ = 'cron'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    status = Column(Integer, nullable=False)
    cron_item = relationship('CronItem', secondary='cron_item_link')


class CronItem(Base):
    """Cron Item model"""
    __tablename__ = 'cron_item'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    schedule = Column(String, nullable=False)
    command = Column(String, nullable=False)
    status = Column(Integer, nullable=False)
    cron = relationship(Cron, secondary='cron_item_link')


class ItemCronLink(Base):
    """Assoc table."""
    __tablename__ = 'cron_item_link'
    cron_id = Column(Integer, ForeignKey('cron.id'), primary_key=True)
    cronitem_id = Column(Integer, ForeignKey('cron_item.id'), primary_key=True)
