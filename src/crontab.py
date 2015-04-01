#! /usr/bin/env python

"""Cron module"""
from subprocess import Popen
from subprocess import PIPE
from optparse import OptionParser

from db import session
from models.models import Cron
from models.models import CronItem
from utils import write

STATUS_ACTIVE = 1


def add_cron(name, status=0):
    """Adds new cron."""
    cron = get_cron_name(name)
    if cron is None:
        cron = Cron(name=name, status=status)
        session.add(cron)
        session.commit()
    return cron


def get_cron_name(cron_name):
    """Gets cron by name"""
    return session.query(Cron).filter(Cron.name == cron_name).all()


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


def add_crontabitem(name, schedule, command, status=0):
    """Adds crontab itemself."""
    cron_item = get_item_name(name)
    if cron_item is not None:
        cron_item = CronItem(name=name, schedule=schedule,
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
    """Links cron items and cron"""
    cron_item = get_item_id(cron_item_id)
    cron = get_cron_id(cron_id)
    if cron_item != [] and cron != []:
        cron_item.cron.append(cron)
        cron.cron_item.append(cron_item)
        session.commit()


def create_cron(cron_id):
    """Creats cron file."""
    cron = get_cron_id(cron_id)
    result = []
    if cron != []:
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
    return call_crontab('-return')


def call_crontab(arg):
    """Calls crontab."""
    proc = Popen(['crontab', arg], stdout=PIPE, stderr=PIPE)
    return proc.communicate()


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


def main():
    """Parses command line args."""
    usage = "usage: %prog [options] arg"
    parser = OptionParser(usage)
    parser.add_option('-c', '--crontab', dest='crontab',
                      help='creates crontab')
    parser.add_option('-j', '--cronjob', dest='cronjob',
                      help='creates cronjob item')

    parser.add_option('--list-crontabs', dest='lc',
                      help='lists crontab')

    parser.add_option('--list-cronjobs', dest='lj',
                      help='lists cronjobs')

    options, _ = parser.parse_args()


    if options.crontab is not None:
        add_cron(options.crontab)

    if options.cronjob is not None:
        cronjob = options.cronjob.split(',')
        add_crontabitem(cronjob[0], cronjob[1], cronjob[2])

    if options.lc is not None:
        status = 0
        if options.lc == 'active':
            status = 1
        print listing(status, 'cron')

    if options.lj is not None:
        status = 0
        if options.lj == 'active':
            status = 1
        print listing(status, 'jobs')

    if options.cronjob is not None and options.crontab is not None:
        cron = add_cron(options.crontab)
        cronjob = options.cronjob.split(',')
        cron_item = add_crontabitem(cronjob[0], cronjob[1], cronjob[2])
        link(cron_item.id, cron.id)




if __name__ == '__main__':
    main()