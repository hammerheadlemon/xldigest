import os

from .models import (DatamapItem, Project, ReturnItem, SeriesItem, Portfolio,
                     Series)

from xldigest.database.setup import set_up_session, USER_DATA_DIR

db_pth = os.path.join(USER_DATA_DIR, 'db.sqlite')
session = set_up_session(db_pth)


def quarter_data(quarter_id):
    d = session.query(DatamapItem.key, ReturnItem.value, Project.id,
                      Project.name, SeriesItem.id).\
        filter(ReturnItem.project_id == Project.id).\
        filter(ReturnItem.series_item_id == SeriesItem.id).\
        filter(ReturnItem.datamap_item_id == DatamapItem.id).all()
    return d


def project_names_per_quarter(quarter_id):
    d = quarter_data(quarter_id)
    projects_in_all_returns = [(item[2], item[3]) for item in d]
    projects_in_all_returns = set(projects_in_all_returns)
    return projects_in_all_returns


def single_project_data(quarter_id, project_id):
    d = quarter_data(quarter_id)
    project_data = [[item[0], item[1]] for item in d if item[2] == project_id]
    return project_data


def project_names_in_portfolio(portfolio_id: int) -> list:
    ps = session.query(Project.name).filter(Portfolio.id == portfolio_id).all()
    return [item[0] for item in ps]


def portfolio_names() -> list:
    pns = session.query(Portfolio.name).all()
    return [item[0] for item in pns]


def series_names() -> list:
    sns = session.query(Series.name).all()
    return [item[0] for item in sns]


def series_items(series: int) -> list:
    """
    Takes a Series id, and returns all SeriesItem objects belonging to it.
    """
    sis = session.query(SeriesItem.name).filter(SeriesItem.series == series).all()
    return [item[0] for item in sis]
