from . sqlalchemy_fixtures import session
from ..database.models import Portfolio

SESSION = session

def test_single_portfolio(SESSION):
    assert SESSION.query(Portfolio.id).first()[0] == 1
    assert SESSION.query(Portfolio.name).first()[0] == "Major Portfolio"

