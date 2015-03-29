"""Cron module"""
from subprocess import Popen
from subprocess import PIPE

from db import session
from models.models import Cron
from models.models import CronItem
from utils import write

STATUS_ACTIVE = 1

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
    return session.query(Cron).filter(Cron.status == STATUS_ACTIVE).all()


def change_cron_status(uuid, status):
    """Sets new status to the cron."""
    cron = get_cron_id(uuid)
    if cron is not None:
        cron.status = status
        session.commit()


def add_crontabitem(name, schedule, command, status=0):
    """Adds crontab itemself."""
    cron_item = CronItem(name=name, schedule=schedule,
                         command=command, status=status)
    session.add(cron_item)
    session.commit()


def get_item_id(uuid):
    """Gets crontab item by id"""
    return session.query(CronItem).filter(CronItem.id == uuid).one()


def link(cron_item_id, cron_id):
    """Links cron items and cron"""
    cron_item = get_item_id(cron_item_id)
    cron = get_cron_id(cron_id)
    if cron_item is not None and cron is not None:
        cron_item.cron.append(cron)
        cron.cron_item.append(cron_item)
        session.commit()


def create_cron(cron_id):
    """Creats cron file."""
    cron = get_cron_id(cron_id)
    result = []
    for item in cron.cron_item:
        if item.status == STATUS_ACTIVE:
            result.append('%s %s' % (item.schedule, item.command))
    return result


def save_cron(cron_id, path='cron'):
    """Saves cron file."""
    write(path, '\n'.join(create_cron(cron_id)))


def activate_cron(path='cron'):
    """Activates cron file."""
    return call_crontab(path)


def remove_cron():
    """Cleanes crontab."""
    return call_crontab('-r')


def call_crontab(arg):
    """Calls crontab."""
    proc = Popen(['crontab', arg], stdout=PIPE, stderr=PIPE)
    return proc.communicate()

