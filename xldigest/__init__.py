from contextlib import contextmanager

import appdirs
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import xldigest.database.models

APPNAME = 'xldigest'
APPAUTHOR = 'MRLemon'
USER_DATA_DIR = appdirs.user_data_dir(APPNAME, APPAUTHOR)
USER_HOME = os.path.expanduser('~')
DB_PATH = os.path.join(USER_DATA_DIR, 'db.sqlite')

if not os.path.exists(USER_DATA_DIR):
    os.makedirs(USER_DATA_DIR)

engine = create_engine("sqlite:///" + DB_PATH)
xldigest.database.models.create_tables(engine)
Session = sessionmaker(bind=engine)
session = Session()

@contextmanager
def session_scope():
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()
