from contextlib import contextmanager

import appdirs
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

import xldigest.database.models

APPNAME = 'xldigest'
APPAUTHOR = 'MRLemon'
USER_DATA_DIR = appdirs.user_data_dir(APPNAME, APPAUTHOR)
USER_HOME = os.path.expanduser('~')
DB_PATH = os.path.join(USER_DATA_DIR, 'db.sqlite')

if not os.path.exists(USER_DATA_DIR):
    os.makedirs(USER_DATA_DIR)

engine = create_engine(("sqlite:///" + DB_PATH), connect_args={'check_same_thread': False}, echo=False)
xldigest.database.models.create_tables(engine)

session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)
session = Session()
