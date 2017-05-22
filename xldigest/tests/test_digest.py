from xldigest.process.template import BICCTemplate
from xldigest.process.datamap import Datamap
from xldigest.process.digest import Digest
from xldigest.process.exceptions import (SeriesItemNotFoundError,
                                         ProjectNotFoundError,
                                         DuplicateReturnError,
                                         NonExistantReturnError)

from xldigest.database.models import (Project, Series, SeriesItem, Portfolio,
                                      ReturnItem)

from tempfile import gettempdir
from openpyxl import load_workbook

import pytest

TMP_DIR = gettempdir()


def test_in_tmp_sqlite3(session):
    q1 = session.query(SeriesItem.name).first()[0]
    p1 = session.query(Project.name).first()[0]
    assert q1 == "Q1 2016/17"
    assert p1 == "A - Project 1"


#@pytest.mark.skip("Flag for removal")
def test_digest_gets_datamap(bicc_return, mock_datamap_source_file, session):
    """Uses cell_map_from_csv() function to process the datamap text file."""
    template = BICCTemplate(bicc_return)
    datamap = Datamap(template, session)
    datamap.cell_map_from_csv(mock_datamap_source_file)
    digest = Digest(datamap, None, None, session)
    assert digest.datamap.cell_map[0].cell_key == 'Project/Programme Name'
    assert digest.datamap.cell_map[2].cell_key == 'GMPP - FD Sign-Off'


def test_digest_gets_project_from_database(session, bicc_return):
    "Get data for a single project from database."
    # P1 Q1 asserts
    qtr_id = 1
    pjt_id = 1
    template = BICCTemplate(bicc_return, False)
    datamap = Datamap(template, session)
    datamap.cell_map_from_database()
    digest = Digest(datamap, qtr_id, pjt_id, session)
    digest.read_project_data()
    assert digest.data[0].cell_key == 'Datamap Key 1'
    assert digest.data[0].cell_value == 'Return Value 1 Project 1 SeriesItem 1'
    assert digest.data[1].cell_value == 'Return Value 2 Project 1 SeriesItem 1'
    assert digest.data[2].cell_value == 'Return Value 3 Project 1 SeriesItem 1'
    # P1 Q2 asserts
    qtr_id = 2
    pjt_id = 1
    template = BICCTemplate(bicc_return, False)
    datamap = Datamap(template, session)
    datamap.cell_map_from_database()
    digest = Digest(datamap, qtr_id, pjt_id, session)
    digest.read_project_data()
    assert digest.data[0].cell_value == 'Return Value 1 Project 1 SeriesItem 2'
    assert digest.data[1].cell_value == 'Return Value 2 Project 1 SeriesItem 2'
    assert digest.data[2].cell_value == 'Return Value 3 Project 1 SeriesItem 2'

    # P2 Q1 asserts
    qtr_id = 1
    pjt_id = 2
    template = BICCTemplate(bicc_return, False)
    datamap = Datamap(template, session)
    datamap.cell_map_from_database()
    digest = Digest(datamap, qtr_id, pjt_id, session)
    digest.read_project_data()
    assert digest.data[0].cell_value == 'Return Value 1 Project 2 SeriesItem 1'
    assert digest.data[1].cell_value == 'Return Value 2 Project 2 SeriesItem 1'
    assert digest.data[2].cell_value == 'Return Value 3 Project 2 SeriesItem 1'

    # P2 Q2 asserts
    qtr_id = 2
    pjt_id = 2
    template = BICCTemplate(bicc_return, False)
    datamap = Datamap(template, session)
    datamap.cell_map_from_database()
    digest = Digest(datamap, qtr_id, pjt_id, session)
    digest.read_project_data()
    assert digest.data[0].cell_value == 'Return Value 1 Project 2 SeriesItem 2'
    assert digest.data[1].cell_value == 'Return Value 2 Project 2 SeriesItem 2'
    assert digest.data[2].cell_value == 'Return Value 3 Project 2 SeriesItem 2'


#@pytest.mark.skip("mark for removal")
def test_digest_reads_return(bicc_return, mock_datamap_source_file, session):
    template = BICCTemplate(bicc_return)
    datamap = Datamap(template, session)
    datamap.cell_map_from_csv(mock_datamap_source_file)
    digest = Digest(datamap, None, None, session)
    # here we need to go through the datamap, use the cell_key and
    # cell_reference to populate the cell_value of the Cell object
    digest.read_template()
    assert digest.data[0].cell_value == 'Cookfield Rebuild'
    assert digest.data[0].cell_reference == 'B5'
    assert digest.data[0].template_sheet == 'Summary'
    assert digest.data[4].cell_value == 2012


def test_missing_series_item(session, bicc_return):
    qtr_id = 100
    pjt_id = 1
    template = BICCTemplate(bicc_return, False)
    datamap = Datamap(template, session)
    datamap.cell_map_from_database()
    digest = Digest(datamap, qtr_id, pjt_id, session)
    with pytest.raises(SeriesItemNotFoundError):
        digest.read_project_data()


def test_missing_project(session, bicc_return):
    qtr_id = 1
    pjt_id = 1000
    template = BICCTemplate(bicc_return, False)
    datamap = Datamap(template, session)
    datamap.cell_map_from_database()
    digest = Digest(datamap, qtr_id, pjt_id, session)
    with pytest.raises(ProjectNotFoundError):
        digest.read_project_data()


def test_both_missing_series_item_project(session, bicc_return):
    """
    This should raise SeriesItemNotFoundError, despite the fact that both
    series_item and project ids are not present.
    """
    qtr_id = 1000
    pjt_id = 1000
    template = BICCTemplate(bicc_return, False)
    datamap = Datamap(template, session)
    datamap.cell_map_from_database()
    digest = Digest(datamap, qtr_id, pjt_id, session)
    with pytest.raises(SeriesItemNotFoundError):
        digest.read_project_data()


def test_populate_blank_form_export_new(test_blank_xls, session):
    qtr_id = 1
    pjt_id = 2
    template = BICCTemplate(test_blank_xls, True)
    datamap = Datamap(template, session)
    datamap.cell_map_from_database()
    digest = Digest(datamap, qtr_id, pjt_id, session)
    output_path = digest.write_to_template(TMP_DIR)
    wb = load_workbook(output_path)
    summary_sheet = wb['Summary']
    assert summary_sheet['B1'].value == 'Return Value 1 Project 2 SeriesItem 1'


def test_populate_blank_form_non_existing_qtr_proj_combo(test_blank_xls, session):
    qtr_id = 30
    pjt_id = 20
    template = BICCTemplate(test_blank_xls, True)
    datamap = Datamap(template, session)
    datamap.cell_map_from_database()
    digest = Digest(datamap, qtr_id, pjt_id, session)
    with pytest.raises(NonExistantReturnError):
        digest.write_to_template(TMP_DIR)


def test_duplicate_record_on_write_to_db(bicc_return, session):
    qtr_id = 1
    pjt_id = 1
    template = BICCTemplate(bicc_return, False)
    datamap = Datamap(template, session)
    datamap.cell_map_from_database()
    digest = Digest(datamap, qtr_id, pjt_id, session)
    digest.read_template()
    with pytest.raises(DuplicateReturnError):
        digest.write_to_database()


def test_attempt_to_write_return_to_db_unavailable_qtr(bicc_return, session):
    qtr_id = 100
    pjt_id = 1
    template = BICCTemplate(bicc_return, False)
    datamap = Datamap(template, session)
    datamap.cell_map_from_database()
    digest = Digest(datamap, qtr_id, pjt_id, session)
    digest.read_template()
    with pytest.raises(SeriesItemNotFoundError):
        digest.write_to_database()


def test_attempt_to_write_return_to_db_unavailable_project(bicc_return, session):
    qtr_id = 1
    pjt_id = 100
    template = BICCTemplate(bicc_return, False)
    datamap = Datamap(template, session)
    datamap.cell_map_from_database()
    digest = Digest(datamap, qtr_id, pjt_id, session)
    digest.read_template()
    with pytest.raises(ProjectNotFoundError):
        digest.write_to_database()


def test_file_name_cleaner(bicc_return, session):
    qtr_id = 1
    pjt_id = 1
    template = BICCTemplate(bicc_return, False)
    datamap = Datamap(template, session)
    datamap.cell_map_from_database()
    digest = Digest(datamap, qtr_id, pjt_id, session)
    digest.read_template()
    assert digest._generate_file_name_from_return_data(
        qtr_id, pjt_id) == 'A___Project_1_Q1_2016_17'


def test_get_project_name_from_digest(bicc_return, session):
    qtr_id = 1
    pjt_id = 1
    template = BICCTemplate(bicc_return, False)
    datamap = Datamap(template, session)
    datamap.cell_map_from_database()
    digest = Digest(datamap, qtr_id, pjt_id, session)
    assert digest.project_name == "A - Project 1"


def test_successful_write_return_to_db(session, bicc_return):
    session.query(ReturnItem).filter(ReturnItem.id > 0).delete(synchronize_session=False)
    qtr_id = 1
    pjt_id = 1
    template = BICCTemplate(bicc_return, False)
    datamap = Datamap(template, session)
    datamap.cell_map_from_database()
    digest = Digest(datamap, qtr_id, pjt_id, session)
    digest.read_template()
    digest._get_existing_return_project_and_series_item_ids()
    digest.write_to_database()
    test_returns = session.query(ReturnItem.value).first()[0]
    assert test_returns == "Return Value 1 Project 1 SeriesItem 1"
