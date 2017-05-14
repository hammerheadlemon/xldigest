import sys

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import xldigest.database
import xldigest.database.paths


class CreateSession:
    def __init__(self):
        self._db_file = xldigest.database.paths.DB_PATH

    def call(self):
        engine_string = "sqlite:///" + self._db_file
        engine = create_engine(engine_string)
        Session = sessionmaker(bind=engine)
        session = Session()
        return session


class CreateSessionWithFile:
    def __init__(self, db_file):
        self._db_file = db_file

    def call(self):
        engine_string = "sqlite:///" + self._db_file
        engine = create_engine(engine_string)
        Session = sessionmaker(bind=engine)
        session = Session()
        return session


class CreateTestSession:
    def __init__(self, file_path: str = None) -> None:
        """
        Pass a string to the file required, or by default creates an in memory database. 
        :param file_path: 
        """
        if file_path:
            self.db_file = file_path
        else:
            self.db_file = "sqlite:///:memory:"

    def call(self):
        setattr(sys.modules['xldigest.database'], 'model_path', self.db_file)
        engine = create_engine('sqlite:///' + self.db_file)
        setattr(sys.modules['xldigest.database.models'], 'engine', engine)
        Session = sessionmaker(bind=engine)
        session = Session()
        return session


class Connection:
    @classmethod
    def session(cls):
        return CreateSession().call()

    @classmethod
    def session_with_file(cls, db_file):
        return CreateSessionWithFile(db_file).call()

    @classmethod
    def session_for_test(cls, db_file):
        return CreateTestSession(db_file).call()
