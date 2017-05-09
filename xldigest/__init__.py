import os

import appdirs

APPNAME = 'xldigest'
APPAUTHOR = 'MRLemon'
USER_DATA_DIR = appdirs.user_data_dir(APPNAME, APPAUTHOR)
USER_HOME = os.path.expanduser('~')
DB_PATH = os.path.join(USER_DATA_DIR, 'db.sqlite')

if not os.path.exists(USER_DATA_DIR):
    os.makedirs(USER_DATA_DIR)


from xldigest.database.models import Portfolio
from xldigest.database.connection import Connection
import xldigest.database.paths

from .startup import main_startup

try:
    SESSION = Connection.session()
except:
    SESSON = None


def test_db():
    session = Connection.session()
    try:
        session.query(Portfolio.id).first()[0] == 1
    except TypeError:
        return False
    return True
