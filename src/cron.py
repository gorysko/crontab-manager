from subprocess import Popen
from subprocess import PIPE

from utils import read
from utils import write


def get_crontab():
    """Gets crontab info."""
    proc = Popen(['crontab', '-l'], stdout=PIPE)
    return proc.communicate()


def add_job(job, path):
    """Adds job to crontab."""
    data = read(path)
    data.append(job + '\n')
    if write(path, ''.join(data)):
        return True
    return False


def activate_cron(path):
    """Activates cron."""
    proc = Popen(['crontab', path], stdout=PIPE)
    if proc:
        return proc.communicate()
    return ()


def remove_cron():
    """Removes cron."""
    proc = Popen(['crontab', '-r'], stdout=PIPE)
    if proc:
        return proc.communicate()
    return ()
