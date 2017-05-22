from xldigest.database.base_queries import check_db_table_duplicates, link_declared_p_name_with_project
from xldigest.widgets.master import DatamapView, DatamapCellItem
from ..database.models import Portfolio, Project, Series, SeriesItem


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


def test_check_db_table_duplicates(session):
    assert check_db_table_duplicates(session) == []


def test_link_declared_p_name_with_project(session):
    assert link_declared_p_name_with_project(1, 1, "Datamap Key 1",
                                             session)[0] == 'Project 1'


def test_datamap_view_object_str(session):
    dmo = DatamapView(1, session)
    assert str(dmo) == "DatamapView for SeriesItem Q1 2016/17"


def test_datamap_view_object_base_cols(session):
    dmo = DatamapView(1, session)
    dmo.add_single_return(1)
    assert dmo.cell_data(0, 0).data == 'DMI'
    assert dmo.cell_data(1, 0).data == 'Key'
    assert dmo.cell_data(0, 1).data == 1
    assert dmo.cell_data(0, 2).data == 2
    DatamapView.returns_added = 0


def test_datamap_view_object_key_col(session):
    dmo = DatamapView(1, session)
    dmo.add_single_return(1)
    assert dmo.cell_data(1, 1).data == 'Datamap Key 1'
    assert dmo.cell_data(1, 2).data == 'Datamap Key 2'
    DatamapView.returns_added = 0


def test_bad_datamap_view_object_access(session):
    dmo = DatamapView(1, session)
    dmo.add_single_return(1)
    assert dmo.cell_data(1, 200) is None
    DatamapView.returns_added = 0


def test_add_second_return(session):
    dmo = DatamapView(1, session)
    dmo.add_single_return(1)
    dmo.add_single_return(2)
    dmo.add_single_return(3)
    assert dmo.cell_data(2, 1).data == 'Return Value 1 Project 1 SeriesItem 1'
    assert dmo.cell_data(3, 1).data == 'Return Value 1 Project 2 SeriesItem 1'
    assert dmo.cell_data(4, 1).data == 'Return Value 1 Project 3 SeriesItem 1'
    DatamapView.returns_added = 0
