"""Cron module"""
from subprocess import Popen
from subprocess import PIPE

from utils import read
from utils import write

def get_crontab():
    """Gets cron info."""
    proc = Popen(['crontab', '-l'], stdout=PIPE)
    return proc.communicate()


def add_job(job, path):
    """Adds cron job"""
    data = read(path)
    data.append(job + '\n')
    if write(path, data):
        return True
    return False


def activate_cron(path):
    """Activates cron file/"""
    proc = Popen(['crontab', path], stdout=PIPE)
    return proc.communicate()


def remove_cron():
    """Removes cron."""
    proc = Popen(['crontab', '-r'], stdout=PIPE)
    return proc.communicate()
