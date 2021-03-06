import os

import appdirs
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

APPNAME = 'xldigest'
APPAUTHOR = 'MRLemon'
USER_DATA_DIR = appdirs.user_data_dir(APPNAME, APPAUTHOR)

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
