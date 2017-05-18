from xldigest.database.base_queries import ReturnSequence, check_db_table_duplicates, link_declared_p_name_with_project
from xldigest.widgets.master import DatamapView, DatamapCellItem
from .sqlalchemy_fixtures import session as SESSION
from ..database.models import Portfolio, Project, Series, SeriesItem


def test_single_portfolio(SESSION):
    assert SESSION.query(Portfolio.id).first()[0] == 1
    assert SESSION.query(Portfolio.name).first()[0] == "Major Portfolio"


def test_single_project(SESSION):
    assert SESSION.query(Project.name).first()[0] == "Project 1"
    assert SESSION.query(Project.name).all()[1][0] == "Project 2"


def test_single_series(SESSION):
    assert SESSION.query(Series.name).first()[0] == "Financial Quarters"


def test_single_series_item(SESSION):
    assert SESSION.query(SeriesItem.name).first()[0] == "Q1 2016/17"


def test_return_sequence(SESSION):
    r = ReturnSequence(1, 1, SESSION)
    r2 = ReturnSequence(2, 2, SESSION)
    r3 = ReturnSequence(1, 10, SESSION)
    r4 = ReturnSequence(8, 68, SESSION)
    assert list(r)[0] == "Return Value 1 Project 1 SeriesItem 1"
    assert list(r2)[0] == "Return Value 2 Project 2 SeriesItem 1"
    assert list(r3)[1] == "Return Value 10 Project 1 SeriesItem 2"
    assert list(r4)[1] == "Return Value 68 Project 8 SeriesItem 2"


def test_check_db_table_duplicates(SESSION):
    assert check_db_table_duplicates(SESSION) == []


def test_link_declared_p_name_with_project(SESSION):
    assert link_declared_p_name_with_project(
        1, 1, "Datamap Key 1", SESSION
    )[0] == 'Project 1'


def test_datamap_view_object_str(SESSION):
    dmo = DatamapView(1, SESSION)
    assert str(dmo) == "DatamapView for SeriesItem Q1 2016/17"

#def test_DatamapCellItem_constructor(SESSION):
#    dci = DatamapCellItem('Project 1', SESSION)


def test_datamap_view_object_add_project_return_data(SESSION):
    dmo = DatamapView(1, SESSION)
    dmo.add_single_return(1)
    assert dmo.cell_data(1, 1) == 'DMI'
    assert dmo.cell_data(2, 1) == 'Key'
    assert dmo.cell_data(1, 2) == 1
    assert dmo.cell_data(1, 3) == 2
