import os

from xldigest.database.models import Portfolio
import xldigest.database.paths

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


if not os.path.exists(xldigest.database.paths.USER_DATA_DIR):
    os.makedirs(xldigest.database.paths.USER_DATA_DIR)


def set_up_session(db_file):
    """
    Helper method to create a SQLAlchemy session.
    """
    engine_string = "sqlite:///" + db_file
    engine = create_engine(engine_string)
    Session = sessionmaker(bind=engine)
    return Session()


try:
    SESSION = set_up_session(xldigest.database.paths.DB_PATH)
except:
    SESSON = None


def test_db():
    session = set_up_session(xldigest.database.paths.DB_PATH)
    try:
        session.query(Portfolio.id).first()[0] == 1
    except TypeError:
        return False
