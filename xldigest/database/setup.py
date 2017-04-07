from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def set_up_session(db_file):
    """
    Helper method to create a SQLAlchemy session.
    """
    engine_string = "sqlite:///" + db_file
    engine = create_engine(engine_string)
    Session = sessionmaker(bind=engine)
    return Session()
