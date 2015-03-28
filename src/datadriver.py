"""Datadriver module."""
import sqlite3

from os import getlogin
from os.path import exists
from os import mkdir
from os.path import isdir
from os.path import abspath
from os.path import join


def get_path(path=None):
    """Gets data path."""
    if path is None:
        path = join(abspath(__file__), '../data/')
    return join(path, getlogin())


def connect(path):
    """Connects to database."""
    if path is None:
        db_path = 'cron.db'
    if path is not None:
        if check_dir(path) is None:
            return None
        db_path = path + 'cron.db'
    return sqlite3.connect(db_path)


def check_dir(path):
    """Checks directory."""
    if exists(path) is False:
        mkdir(path)
        return True
    if isdir(path) is False:
        return True

    return False


def put_data(path, data):
    """Saves data to database."""
    pass


def get_data(path):
    """Gets data from database."""
    pass

