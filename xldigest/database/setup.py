import os

from xldigest.database.models import Portfolio
from xldigest.database.connection import Connection
import xldigest.database.paths

if not os.path.exists(xldigest.database.paths.USER_DATA_DIR):
    os.makedirs(xldigest.database.paths.USER_DATA_DIR)

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
