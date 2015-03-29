"""Cron module"""
from subprocess import Popen
from subprocess import PIPE

from db import session

from models.cron import Cron
from models.cron_item import CronItem


def add_cron(name, status=0):
    """Adds new cron."""
    cron = Cron(name=name, status=status)
    session.add(cron)
    session.commit()


def get_cron_name(cron_name):
    """Gets cron by name"""
    return session.query(Cron).filter(Cron.name == cron_name).all()


def get_cron_id(uuid):
    """Gets cron by uuid."""
    return session.query(Cron).filter(Cron.id == uuid).one()


def get_active():
    """Gets all active crons."""
    return session.query(Cron).filter(Cron.status == 1).all()


def change_status(uuid, status):
    """Sets new status to the cron."""
    cron = get_cron_id(uuid)
    if cron is not None:
        cron.status = status
        session.commit()
