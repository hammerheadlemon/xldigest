from xldigest.database.base_queries import ReturnSequence
from .sqlalchemy_fixtures import session
from ..database.models import Portfolio, Project, Series, SeriesItem

session = session


def test_single_portfolio(session):
    assert session.query(Portfolio.id).first()[0] == 1
    assert session.query(Portfolio.name).first()[0] == "Major Portfolio"


def test_single_project(session):
    assert session.query(Project.name).first()[0] == "Project 1"
    assert session.query(Project.name).all()[1][0] == "Project 2"


def test_single_series(session):
    assert session.query(Series.name).first()[0] == "Financial Quarters"


def test_single_series_item(session):
    assert session.query(SeriesItem.name).first()[0] == "Q1 2016/17"


def test_return_sequence(session):
    r = ReturnSequence(1, 1, session)
    r2 = ReturnSequence(2, 2, session)
    r3 = ReturnSequence(1, 10, session)
    r4 = ReturnSequence(8, 68, session)
    assert list(r)[0] == "Return Value 1 Project 1 SeriesItem 1"
    assert list(r2)[0] == "Return Value 2 Project 2 SeriesItem 1"
    assert list(r3)[1] == "Return Value 10 Project 1 SeriesItem 2"
    assert list(r4)[1] == "Return Value 68 Project 8 SeriesItem 2"
