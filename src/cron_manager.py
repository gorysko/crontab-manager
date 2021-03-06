#! /usr/bin/env python

"""Cron module"""
from subprocess import Popen
from subprocess import PIPE

from db import session
from models.models import Cron
from models.models import CronItem
from utils import write


STATUS_DISABLED = 0
STATUS_ACTIVE = 1
STATUS_RUNNING = 2

SCHEDULE = {
    'daily': '0 0 0 0 *',
    'workdays': '0 0 * * 1-5',
    'weekends': '0 0 * * 6-7',
    'monthly': '0 0 1 * *',
    'workhours': '0 09-18 * * 1-5'
}


def add_cron(name, status=STATUS_DISABLED):
    """Adds new cron."""
    cron = get_cron_name(name)
    if cron is None:
        cron = Cron(name=name, status=status)
        session.add(cron)
        session.commit()
    return cron


def get_cron_name(cron_name):
    """Gets cron by name."""
    return session.query(Cron).filter(Cron.name == cron_name).all()


def get_cron_jobs(cron_id):
    """Gets cron jobs of the cron."""
    cron = get_cron_id(cron_id)
    if cron is not None:
        return [item.name for item in cron.cron_item]
    return []


def get_cron_id(uuid):
    """Gets cron by uuid."""
    result = session.query(Cron).filter(Cron.id == uuid)
    if result.count() != 0:
        return result.one()
    return []


def get_crontabs(status):
    """Gets alls crons."""
    return session.query(Cron).filter(Cron.status == status).all()


def change_cron_status(uuid, status):
    """Sets new status to the cron."""
    cron = get_cron_id(uuid)
    if cron is not None:
        cron.status = status
        session.commit()
        return True
    return False


def add_crontabitem(name, schedule, command, status=STATUS_DISABLED):
    """Adds crontab itemself."""
    cron_item = get_item_name(name)
    timing = schedule
    if schedule in SCHEDULE:
        timing = SCHEDULE[schedule]
    if cron_item is not None:
        cron_item = CronItem(name=name, schedule=timing,
                             command=command, status=status)
        session.add(cron_item)
        session.commit()
    return cron_item


def get_item_name(name):
    """Gets crontab item by name"""
    result = session.query(CronItem).filter(CronItem.name == name)
    if result.count() != 0:
        return result.one()
    return []


def get_item_id(uuid):
    """Gets crontab item by id"""
    return session.query(CronItem).filter(CronItem.id == uuid).one()


def link(cron_item_id, cron_id):
    """Links cron items and cron
    Args:
        cron_item_id: uuid of the cron item
        cron: uuid of the cron
    """
    cron_item = get_item_id(cron_item_id)
    cron = get_cron_id(cron_id)
    if cron_item != [] and cron != []:
        cron_item.cron.append(cron)
        cron.cron_item.append(cron_item)
        session.commit()
        return True
    return False


def create_cron(cron_id):
    """Creats cron file.
    Args:
        cron_id: uuid of the cron.
    """
    cron = get_cron_id(cron_id)
    result = []
    if cron != []:
        for item in cron.cron_item:
            if item.status == STATUS_ACTIVE:
                result.append('%s %s' % (item.schedule, item.command))
    return result


def activate_cron(cron_id, path='cron'):
    """Activates cron by cron_id.
    Args:
        cron_id: id of the cron to b activated.
        path: path for the cron file template.
    """
    if change_cron_status(cron_id, STATUS_RUNNING):
        return save_cron(cron_id, path) and run_cron(path)
    return False


def save_cron(cron_id, path='cron'):
    """Saves cron file.
    Args:
        cron_id: id of the cron to be saved in template.
        path: path for the saving template.
    """
    result = create_cron(cron_id)
    if result != []:
        write(path, '\n'.join(result))
        return True
    return False


def run_cron(path='cron'):
    """Runs cron file.
    Args:
        path: path to cron template, file.
    """
    return _call_crontab(path)


def remove_cron():
    """Cleanes crontab."""
    return _call_crontab('-r')


def list_crontabs(status=STATUS_ACTIVE):
    """Listing of crontabs."""
    items = get_crontabs(status)
    return [item.name for item in items]


def get_cronjobs(status):
    """gets list of cronjobs"""
    return session.query(CronItem).filter(CronItem.status == status).all()


def listing(status=STATUS_ACTIVE, value='cron'):
    """Lists cronjobs."""
    actions = {'cron': get_crontabs, 'jobs': get_cronjobs}
    items = actions[value](status)
    return [item.name for item in items]


def _call_crontab(arg):
    """Calls crontab."""
    proc = Popen(['crontab', arg], stdout=PIPE, stderr=PIPE)
    return proc.communicate()
