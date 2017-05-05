from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class _CreateSession:
    def __init__(self, db_file):
        self._db_file = db_file

    def call(self):
        engine_string = "sqlite:///" + self._db_file
        engine = create_engine(engine_string)
        return sessionmaker(bind=engine)


class Connection:

    @classmethod
    def session(cls, db_file):
        return _CreateSession(db_file)
