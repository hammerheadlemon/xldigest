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
