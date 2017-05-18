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

def test_datamap_view_object_base_cols(SESSION):
    dmo = DatamapView(1, SESSION)
    dmo.add_single_return(1)
    assert dmo.cell_data(0, 0) == 'DMI'
    assert dmo.cell_data(1, 0) == 'Key'
    assert dmo.cell_data(0, 1) == 1
    assert dmo.cell_data(0, 2) == 2
    DatamapView.returns_added = 0


def test_datamap_view_object_key_col(SESSION):
    dmo = DatamapView(1, SESSION)
    dmo.add_single_return(1)
    assert dmo.cell_data(1, 1) == 'Datamap Key 1'
    assert dmo.cell_data(1, 2) == 'Datamap Key 2'
    DatamapView.returns_added = 0

def test_bad_datamap_view_object_access(SESSION):
    dmo = DatamapView(1, SESSION)
    dmo.add_single_return(1)
    assert dmo.cell_data(1, 200) == None
    DatamapView.returns_added = 0

def test_add_second_return(SESSION):
    dmo = DatamapView(1, SESSION)
    dmo.add_single_return(1)
    dmo.add_single_return(2)
    assert dmo.cell_data(2, 1) == 'Return Value 1 Project 1 SeriesItem 1'
    assert dmo.cell_data(3, 1) == 'Return Value 1 Project 2 SeriesItem 1'
    DatamapView.returns_added = 0
