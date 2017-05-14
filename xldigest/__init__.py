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


# REFACTORING SESSION-HANDLING = this belongs to 9da82e5, where
# I started to the refactor

#from xldigest.database.models import Portfolio
#from xldigest.database.connection import Connection
#import xldigest.database.paths
#
#from .startup import main_startup
#
#try:
#    SESSION = Connection.session()
#except:
#    SESSON = None
#
#
#def test_db():
#    session = Connection.session()
#    try:
#        session.query(Portfolio.id).first()[0] == 1
#    except TypeError:
#        return False
#    return True
