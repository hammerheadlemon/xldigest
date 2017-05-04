import os

from pathlib import Path

import appdirs

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker



APPNAME = 'xldigest'
APPAUTHOR = 'MRLemon'
USER_DATA_DIR = appdirs.user_data_dir(APPNAME, APPAUTHOR)
USER_HOME = os.path.expanduser('~')
DB_PATH = os.path.join(USER_DATA_DIR, 'db.sqlite')

if not os.path.exists(USER_DATA_DIR):
    os.makedirs(USER_DATA_DIR)


def set_up_session(db_file):
    """
    Helper method to create a SQLAlchemy session.
    """
    engine_string = "sqlite:///" + db_file
    engine = create_engine(engine_string)
    Session = sessionmaker(bind=engine)
    return Session()


try:
    SESSION = set_up_session(DB_PATH)
except:
    SESSON = None


def test_db():
    from xldigest.database.models import Portfolio
    session = set_up_session(DB_PATH)
    try:
        session.query(Portfolio.name).all()
        SESSION = session
    except:
        pass


test_db()
