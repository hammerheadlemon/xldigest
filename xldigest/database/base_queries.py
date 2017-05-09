from xldigest.database.connection import Connection
from .models import (DatamapItem, Project, ReturnItem, SeriesItem, Portfolio,
                     Series)


def quarter_data(quarter_id):
    session = Connection.session()
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
    session = Connection.session()
    ps = session.query(Project.name).filter(Portfolio.id == portfolio_id).all()
    return [item[0] for item in ps]


def portfolio_names() -> list:
    session = Connection.session()
    pns = session.query(Portfolio.name).all()
    return [item[0] for item in pns]


def project_ids_in_returns_with_series_item_of(series_item_id: int) -> list:
    session = Connection.session()
    return list(set([x[0] for x in session.query(
        ReturnItem.project_id).filter(
            ReturnItem.series_item_id == series_item_id).all()]))


def projects_with_id() -> dict:
    session = Connection.session()
    tups = session.query(Project.name, Project.id).all()
    return {tupe[0]: tupe[1] for tupe in tups}


def series_names() -> list:
    session = Connection.session()
    sns = session.query(Series.name).all()
    return [item[0] for item in sns]


def get_project_id(project_name) -> int:
    session = Connection.session()
    id = session.query(Project.id).filter(
        Project.name == project_name).first()[0]
    return id


def series_items(series: int) -> list:
    session = Connection.session()
    """
    Takes a Series id, and returns all SeriesItem objects belonging to it.
    """
    sis = session.query(SeriesItem.name).filter(SeriesItem.series == series).all()
    return [item[0] for item in sis]
