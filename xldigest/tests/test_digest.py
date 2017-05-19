from xldigest.process.template import BICCTemplate
from xldigest.process.datamap import Datamap
from xldigest.process.digest import Digest
from xldigest.process.exceptions import (SeriesItemNotFoundError,
                                         ProjectNotFoundError,
                                         DuplicateReturnError,
                                         NonExistantReturnError)
from xldigest.tests.fixtures import TMP_DIR
from xldigest.tests.sqlalchemy_fixtures import session as SESSION

from xldigest.database.models import (Project, Series, SeriesItem, Portfolio,
                                      ReturnItem)

from openpyxl import load_workbook

import xldigest.tests.fixtures as fixtures
import pytest


BICC_RETURN_MOCK = fixtures.bicc_return
DATAMAP_MOCK = fixtures.mock_datamap_source_file
TEST_BLANK_XLS = fixtures.test_blank_xls


def test_in_tmp_sqlite3(SESSION):
    q1 = SESSION.query(SeriesItem.name).first()[0]
    p1 = SESSION.query(Project.name).first()[0]
    assert q1 == "Q1 2016/17"
    assert p1 == "Project 1"


def test_digest_gets_datamap(BICC_RETURN_MOCK, DATAMAP_MOCK, SESSION):
    """Uses cell_map_from_csv() function to process the datamap text file."""
    template = BICCTemplate(BICC_RETURN_MOCK)
    datamap = Datamap(template, SESSION)
    datamap.cell_map_from_csv(DATAMAP_MOCK)
    digest = Digest(datamap, None, None, SESSION)
    assert digest.datamap.cell_map[0].cell_key == 'Project/Programme Name'
    assert digest.datamap.cell_map[2].cell_key == 'GMPP - FD Sign-Off'


def test_digest_gets_project_from_database(SESSION):
    "Get data for a single project from database."
    # P1 Q1 asserts
    qtr_id = 1
    pjt_id = 1
    template = BICCTemplate(BICC_RETURN_MOCK, False)
    datamap = Datamap(template, SESSION)
    datamap.cell_map_from_database()
    digest = Digest(datamap, qtr_id, pjt_id, SESSION)
    digest.read_project_data()
    print()
    print(digest.data[0])
    print(digest.data[1])
    print(digest.data[2])
    print(digest.data[3])
    assert digest.data[0].cell_key == 'Datamap Key 1'
    assert digest.data[0].cell_value[
        0] == 'Return Value 1 Project 1 SeriesItem 1'
    assert digest.data[1].cell_value[0] == 'Return Value 2 Project 1 SeriesItem 1'
    assert digest.data[2].cell_value[0] == 'Return Value 3 Project 1 SeriesItem 1'
    # P1 Q2 asserts
    qtr_id = 2
    pjt_id = 1
    template = BICCTemplate(BICC_RETURN_MOCK, False)
    datamap = Datamap(template, SESSION)
    datamap.cell_map_from_database()
    digest = Digest(datamap, qtr_id, pjt_id, SESSION)
    digest.read_project_data()
    print()
    print(digest.data[0])
    print(digest.data[1])
    print(digest.data[2])
    print(digest.data[3])
    assert digest.data[0].cell_value[
        0] == 'Return Value 1 Project 1 SeriesItem 2'
    assert digest.data[1].cell_value[0] == 'Return Value 2 Project 1 SeriesItem 2'
    assert digest.data[2].cell_value[0] == 'Return Value 3 Project 1 SeriesItem 2'

    # P2 Q1 asserts
    qtr_id = 1
    pjt_id = 2
    template = BICCTemplate(BICC_RETURN_MOCK, False)
    datamap = Datamap(template, SESSION)
    datamap.cell_map_from_database()
    digest = Digest(datamap, qtr_id, pjt_id, SESSION)
    digest.read_project_data()
    print()
    print(digest.data[0])
    print(digest.data[1])
    print(digest.data[2])
    print(digest.data[3])
    assert digest.data[0].cell_value[
        0] == 'Return Value 1 Project 2 SeriesItem 1'
    assert digest.data[1].cell_value[0] == 'Return Value 2 Project 2 SeriesItem 1'
    assert digest.data[2].cell_value[0] == 'Return Value 3 Project 2 SeriesItem 1'

    # P2 Q2 asserts
    qtr_id = 2
    pjt_id = 2
    template = BICCTemplate(BICC_RETURN_MOCK, False)
    datamap = Datamap(template, SESSION)
    datamap.cell_map_from_database()
    digest = Digest(datamap, qtr_id, pjt_id, SESSION)
    digest.read_project_data()
    print()
    print(digest.data[0])
    print(digest.data[1])
    print(digest.data[2])
    print(digest.data[3])
    assert digest.data[0].cell_value[0] == 'Return Value 1 Project 2 SeriesItem 2'
    assert digest.data[1].cell_value[0] == 'Return Value 2 Project 2 SeriesItem 2'
    assert digest.data[2].cell_value[0] == 'Return Value 3 Project 2 SeriesItem 2'


def test_digest_reads_return(BICC_RETURN_MOCK, DATAMAP_MOCK, SESSION):
    template = BICCTemplate(BICC_RETURN_MOCK)
    datamap = Datamap(template, SESSION)
    datamap.cell_map_from_csv(DATAMAP_MOCK)
    digest = Digest(datamap, None, None, SESSION)
    # here we need to go through the datamap, use the cell_key and
    # cell_reference to populate the cell_value of the Cell object
    digest.read_template()
    #print("\n")
    #for cell in digest.data:
    #    try:
    #        print("{0:<70}{1:<30}{2:<70}".format(
    #            cell.cell_key, cell.template_sheet, cell.cell_value))
    #    except Exception:
    #        pass
    # WARNING: digest.data[] index here depends on whether the cell_reference
    # is not None. Cell objects whose cell_reference value is None
    # will NOT be migrated into the Digest object, therefore the order of
    # Cell objects in the .data member will vary depending on the Datamap.
    assert digest.data[0].cell_value == 'Cookfield Rebuild'
    assert digest.data[0].cell_reference == 'B5'
    assert digest.data[0].template_sheet == 'Summary'
    assert digest.data[4].cell_value == 2012


def test_missing_series_item(SESSION):
    qtr_id = 100
    pjt_id = 1
    template = BICCTemplate(BICC_RETURN_MOCK, False)
    datamap = Datamap(template, SESSION)
    datamap.cell_map_from_database()
    digest = Digest(datamap, qtr_id, pjt_id, SESSION)
    with pytest.raises(SeriesItemNotFoundError):
        digest.read_project_data()


def test_missing_project(SESSION):
    qtr_id = 1
    pjt_id = 1000
    template = BICCTemplate(BICC_RETURN_MOCK, False)
    datamap = Datamap(template, SESSION)
    datamap.cell_map_from_database()
    digest = Digest(datamap, qtr_id, pjt_id, SESSION)
    with pytest.raises(ProjectNotFoundError):
        digest.read_project_data()


def test_both_missing_series_item_project(SESSION):
    """
    This should raise SeriesItemNotFoundError, despite the fact that both
    series_item and project ids are not present.
    """
    qtr_id = 1000
    pjt_id = 1000
    template = BICCTemplate(BICC_RETURN_MOCK, False)
    datamap = Datamap(template, SESSION)
    datamap.cell_map_from_database()
    digest = Digest(datamap, qtr_id, pjt_id, SESSION)
    with pytest.raises(SeriesItemNotFoundError):
        digest.read_project_data()


def test_populate_blank_form_export_new(TEST_BLANK_XLS, SESSION):
    qtr_id = 1
    pjt_id = 2
    template = BICCTemplate(TEST_BLANK_XLS, True)
    datamap = Datamap(template, SESSION)
    datamap.cell_map_from_database()
    digest = Digest(datamap, qtr_id, pjt_id, SESSION)
    output_path = digest.write_to_template(TMP_DIR)
    wb = load_workbook(output_path)
    summary_sheet = wb['Summary']
    assert summary_sheet['B1'].value == 'Return Value 1 Project 2 SeriesItem 1'


def test_populate_blank_form_non_existing_qtr_proj_combo(TEST_BLANK_XLS, SESSION):
    qtr_id = 30
    pjt_id = 20
    template = BICCTemplate(TEST_BLANK_XLS, True)
    datamap = Datamap(template, SESSION)
    datamap.cell_map_from_database()
    digest = Digest(datamap, qtr_id, pjt_id, SESSION)
    with pytest.raises(NonExistantReturnError):
        digest.write_to_template(TMP_DIR)


def test_duplicate_record_on_write_to_db(BICC_RETURN_MOCK, SESSION):
    qtr_id = 1
    pjt_id = 1
    template = BICCTemplate(BICC_RETURN_MOCK, False)
    datamap = Datamap(template, SESSION)
    datamap.cell_map_from_database()
    digest = Digest(datamap, qtr_id, pjt_id, SESSION)
    digest.read_template()
    with pytest.raises(DuplicateReturnError):
        digest.write_to_database()


def test_attempt_to_write_return_to_db_unavailable_qtr(BICC_RETURN_MOCK, SESSION):
    qtr_id = 100
    pjt_id = 1
    template = BICCTemplate(BICC_RETURN_MOCK, False)
    datamap = Datamap(template, SESSION)
    datamap.cell_map_from_database()
    digest = Digest(datamap, qtr_id, pjt_id, SESSION)
    digest.read_template()
    with pytest.raises(SeriesItemNotFoundError):
        digest.write_to_database()


def test_attempt_to_write_return_to_db_unavailable_project(BICC_RETURN_MOCK, SESSION):
    qtr_id = 1
    pjt_id = 100
    template = BICCTemplate(BICC_RETURN_MOCK, False)
    datamap = Datamap(template, SESSION)
    datamap.cell_map_from_database()
    digest = Digest(datamap, qtr_id, pjt_id, SESSION)
    digest.read_template()
    with pytest.raises(ProjectNotFoundError):
        digest.write_to_database()


def test_file_name_cleaner(BICC_RETURN_MOCK, SESSION):
    qtr_id = 1
    pjt_id = 1
    template = BICCTemplate(BICC_RETURN_MOCK, False)
    datamap = Datamap(template, SESSION)
    datamap.cell_map_from_database()
    digest = Digest(datamap, qtr_id, pjt_id, SESSION)
    digest.read_template()
    assert digest._generate_file_name_from_return_data(
        qtr_id, pjt_id) == 'Project_1_Q1_2016_17'


def test_get_project_name_from_digest(BICC_RETURN_MOCK, SESSION):
    qtr_id = 1
    pjt_id = 1
    template = BICCTemplate(BICC_RETURN_MOCK, False)
    datamap = Datamap(template, SESSION)
    datamap.cell_map_from_database()
    digest = Digest(datamap, qtr_id, pjt_id, SESSION)
    assert digest.project_name == "Project 1"


def test_successful_write_return_to_db(SESSION, BICC_RETURN_MOCK):
    SESSION.query(ReturnItem).filter(ReturnItem.id > 0).delete(synchronize_session=False)
    qtr_id = 1
    pjt_id = 1
    template = BICCTemplate(BICC_RETURN_MOCK, False)
    datamap = Datamap(template, SESSION)
    datamap.cell_map_from_database()
    digest = Digest(datamap, qtr_id, pjt_id, SESSION)
    digest.read_template()
    digest._get_existing_return_project_and_series_item_ids()
    digest.write_to_database()
    test_returns = SESSION.query(ReturnItem.value).first()[0]
    assert test_returns == "Return Value 1 Project 1 SeriesItem 1"
