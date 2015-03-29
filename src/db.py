"""DB module."""
from sqlalchemy import create_engine

from models import Base
from models import cron
from models import cron_item


engine = create_engine('sqlite:///cron.db')
Base.metadata.create_all(engine, checkfirst=True)
