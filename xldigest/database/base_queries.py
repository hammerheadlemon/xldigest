from .models import DatamapItem, Project, Quarter, ReturnItem

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

engine = create_engine('sqlite:////home/lemon/code/python/xldigest/'
                       'xldigest/db.sqlite')

Session = sessionmaker(bind=engine)
session = scoped_session(Session)


def quarter_data(quarter_id):
    d = session.query(DatamapItem.key, ReturnItem.value, Project.id,
                      Project.name, Quarter.id).\
        filter(ReturnItem.project_id == Project.id).\
        filter(ReturnItem.quarter_id == Quarter.id).\
        filter(ReturnItem.datamap_item_id == DatamapItem.id).\
        filter(ReturnItem.quarter_id == quarter_id).all()
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
