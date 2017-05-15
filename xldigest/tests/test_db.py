from .sqlalchemy_fixtures import session
from ..database.models import Portfolio, Project

session = session


def test_single_portfolio(session):
    assert session.query(Portfolio.id).first()[0] == 1
    assert session.query(Portfolio.name).first()[0] == "Major Portfolio"


def test_single_project(session):
    assert session.query(Project.name).first()[0] == "Project 1"
    assert session.query(Project.name).all()[1][0] == "Project 2"
