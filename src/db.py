"""DB module."""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Base
from models.cron import Cron
from models.cron_item import CronItem

# creating engine
engine = create_engine('sqlite:///cron.db')
Base.metadata.create_all(engine, checkfirst=True)

# dbsession
DBSession = sessionmaker(bind=engine)
session = DBSession()
