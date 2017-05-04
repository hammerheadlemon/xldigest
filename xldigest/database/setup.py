import os

from pathlib import Path

import appdirs

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


APPNAME = 'xldigest'
APPAUTHOR = 'MRLemon'
USER_DATA_DIR = appdirs.user_data_dir(APPNAME, APPAUTHOR)
USER_HOME = os.path.expanduser('~')
DB_PATH = None
SESSION = None

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


def test_db():
    if Path(USER_DATA_DIR + '/db.sqlite').is_file():
        DB_PATH = os.path.join(USER_DATA_DIR, 'db.sqlite')
        SESSION = set_up_session(DB_PATH)
        return True
    else:
        SESSION = None
        DB_PATH = None
        return False


DATABASE_PRESENT = test_db()
