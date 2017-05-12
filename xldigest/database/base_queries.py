from collections import namedtuple, Counter
from operator import itemgetter

from xldigest.database.connection import Connection
from .models import (DatamapItem, Project, ReturnItem, SeriesItem, Portfolio,
                     Series)


class ReturnSequence:
    """
    Sequence of return values given a project_id and series_item_id.

    >> r = ReturnSequence(1, 1) # project_id 1, datamap_item_id 1
    >> list(r) # ['200', '300'] (there are two returns for that project in db)

    """

    def __init__(self, project_id, dm_key_id):
        self.project_id = project_id
        self.dm_key_id = dm_key_id
        self._data = self._collect()

    def _collect(self):
        session = Connection.session()
        ReturnLine = namedtuple('ReturnLine', [
            'project_name', 'project_id', 'series_item_name', 'series_item_id',
            'key_name', 'key_id', 'value'
        ])
        try:
            rows = session.query(
                Project.name, Project.id, SeriesItem.name, SeriesItem.id,
                DatamapItem.key, DatamapItem.id, ReturnItem.value).join(
                    ReturnItem, DatamapItem, SeriesItem).filter(
                        Project.id == self.project_id,
                        DatamapItem.id == self.dm_key_id)
            return [ReturnLine._make(row) for row in rows]
        except:
            raise

    def __getitem__(self, index):
        return self.data[index].value

    def __iter__(self):
        for item in self._data:
            yield item.value
        return

    @property
    def data(self):
        return self._data


def check_db_table_duplicates(model_instance):
    """
    Function which counts the ids of model objects and returns the list
    of any duplicates.
    """
    session = Connection.session()
    c = [
        item for item, count in Counter(session.query(DatamapItem.id)).items()
        if count > 1
    ]
    return c


def link_declared_p_name_with_project(series_item_id: int,
                                      project_id: int,
                                      dm_key: str) -> tuple:
    session = Connection.session()
    return session.query(Project.name, ReturnItem.value).join(
        ReturnItem,
        DatamapItem).filter(ReturnItem.series_item_id == series_item_id,
                            ReturnItem.project_id == project_id,
                            DatamapItem.key == dm_key).first()


def link_projects_all_in_return(series_item_id: int) -> tuple:
    ps = project_ids_in_returns_with_series_item_of(series_item_id)
    t = []
    for p in ps:
        t.append(
            link_declared_p_name_with_project(series_item_id, p,
                                              "Project/Programme Name"))
    return t


def create_master_friendly_header(submitted_titles: list,
                                  series_item_id: int) -> list:
    return sorted([
        i[0]
        for i in link_projects_all_in_return(series_item_id)
        for t in submitted_titles if t == i[1]
    ])


def forumulate_data_for_master_model(
        series_item_id: int,
        project_ids: list,
        dm_keys: list, ) -> list:
    """
    Returns a list of (v1, v2, v3, ..) tuples where vn is the corresponding
    value in each return that matches all the project_ids for a particular
    series_item.
    """
    session = Connection.session()
    dm_ids = session.query(DatamapItem.id).all()
    dm_ids = [i[0] for i in dm_ids]
    collect = []
    for i in list(project_ids):
        db_items = session.query(ReturnItem.value).filter(
            ReturnItem.series_item_id == series_item_id,
            ReturnItem.project_id == i).all()
        db_items_lst = [item[0] for item in db_items]
        collect.append(db_items_lst)
    # sort the raw data into alphabetical order based on declared Project name
    collect = sorted(collect, key=itemgetter(0))
    # time to flip into tuples of related values ("A13", "Bound Materials",..)
    flipped = list(zip(dm_ids, dm_keys, *collect))
    return flipped


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


def portfolio_names() -> tuple:
    """You get the id as the first value in the tuple for free..."""
    session = Connection.session()
    pns = session.query(Portfolio.id, Portfolio.name).all()
    return [item for item in pns]


def project_ids_in_returns_with_series_item_of(series_item_id: int) -> list:
    session = Connection.session()
    return list(
        set([
            x[0]
            for x in session.query(ReturnItem.project_id).filter(
                ReturnItem.series_item_id == series_item_id).all()
        ]))


def datamap_items_in_return(series_item_id: int, project_id: int) -> list:
    session = Connection.session()
    return [
        item[0]
        for item in session.query(DatamapItem.key).join(ReturnItem).filter(
            ReturnItem.series_item_id == series_item_id, ReturnItem.project_id
            == project_id).all()
    ]


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


def series_item_ids_in_returns() -> list:
    """Returns list of tuple of series_item names and ids in all returns"""
    session = Connection.session()
    return list(set(session.query(SeriesItem.id, SeriesItem.name).join(ReturnItem).all()))


def series_items(series: int) -> list:
    session = Connection.session()
    """
    Takes a Series id, and returns all SeriesItem objects belonging to it.
    """
    sis = session.query(SeriesItem.name).filter(
        SeriesItem.series == series).all()
    return [item[0] for item in sis]
