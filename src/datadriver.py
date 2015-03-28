"""Datadriver module."""
import sqlite3

from os.path import isdir

def connect(path):
    """Connects to database."""
    if path is None:
        db_path = 'cron.db'
    if path is not None:
        if isdir(path) is None:
            return None
        db_path = path + 'cron.db'
    return sqlite3.connect(db_path)
