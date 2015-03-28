"""Datadriver module."""
import sqlite3

from os import getlogin

from os import mkdir
from os.path import dirname
from os.path import exists
from os.path import isdir
from os.path import abspath
from os.path import join


def get_path(path=None):
    """Gets data path."""
    if path is None:
        path = join(dirname(abspath(__file__)), '../data/')
    return path


def connect():
    """Connects to database."""
    path = get_path()
    if path is None:
        db_path = 'cron.db'
    if path is not None:
        if check_dir(path) is None:
            return None
        db_path = path + 'cron.db'
    return sqlite3.connect(db_path)


def connection_open():
    """Returns cursor."""
    conn = connect()
    if conn is not None:
        return conn

def connection_close(connection):
    """Commits and closes connection."""
    return connection.commit() and connection.close()


def migrate():
    """Migrates database."""
    connection = connection_open()
    cursor = connection.cursor()
    if cursor is not None:
        command = ('CREATE TABLE crons'
                   '(schedule text, command text,'
                   ' status int, login text)')
        cursor.execute(command)
        connection_close(connection)


def add_value(schedule, command, status, login):
    """Inserts data into database."""
    connection = connection_open()
    cursor = connection.cursor()
    if cursor is not None:
        command = ('''INSERT INTO crons VALUES'
                   ' ('%s','%s','%d','%s')''') % (schedule, command,
                                                  status, login)
        cursor.execute(command)
        connection_close(connection)

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

