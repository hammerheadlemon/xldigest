import xldigest.database.paths

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class CreateSession:
    def __init__(self):
        self._db_file = xldigest.database.paths.DB_PATH

    def call(self):
        engine_string = "sqlite:///" + self._db_file
        engine = create_engine(engine_string)
        Session = sessionmaker(bind=engine)
        session = Session()
        return session


class Connection:

    @classmethod
    def session(cls):
        return CreateSession().call()
