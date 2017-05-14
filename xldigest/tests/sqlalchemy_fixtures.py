import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import xldigest.database.models as models

engine = create_engine("sqlite:///" + ':memory:')
Session = sessionmaker(bind=engine)

models.create_tables(engine)

@pytest.fixture()
def session() -> Session:
    session = Session()
    portfolio = models.Portfolio(name="Major Portfolio")
    session.add(portfolio)
    session.commit()
    yield session
    session.close()

