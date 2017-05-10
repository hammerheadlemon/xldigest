from xldigest.process.template import BICCTemplate
from xldigest.process.datamap import Datamap
from xldigest.process.digest import Digest
from xldigest.process.exceptions import (SeriesItemNotFoundError,
                                         ProjectNotFoundError,
                                         DuplicateReturnError,
                                         NonExistantReturnError)
from xldigest.tests.fixtures import TMP_DIR

from openpyxl import load_workbook

import xldigest.tests.fixtures as fixtures
import pytest
import sqlite3


BICC_RETURN_MOCK = fixtures.bicc_return
DATAMAP_MOCK = fixtures.mock_datamap_source_file
INMEMORY_SQLITE3 = fixtures.sqlite3_db_file
TEST_BLANK_XLS = fixtures.test_blank_xls


def test_in_tmp_sqlite3(INMEMORY_SQLITE3):
    conn = sqlite3.connect(INMEMORY_SQLITE3)
    c = conn.cursor()
    q1 = c.execute("SELECT * FROM series_items").fetchone()[1]
    p1 = c.execute("SELECT * FROM projects").fetchone()[1]
    assert q1 == "Q1 2013/14"
    assert p1 == "Project 1"


def test_digest_gets_datamap(BICC_RETURN_MOCK, DATAMAP_MOCK, INMEMORY_SQLITE3):
    """Uses cell_map_from_csv() function to process the datamap text file."""
    template = BICCTemplate(BICC_RETURN_MOCK)
    datamap = Datamap(template,
                      INMEMORY_SQLITE3)
    datamap.cell_map_from_csv(DATAMAP_MOCK)
    digest = Digest(datamap, None, None)
    assert digest.datamap.cell_map[0].cell_key == 'Project/Programme Name'
    assert digest.datamap.cell_map[2].cell_key == 'GMPP - FD Sign-Off'


@pytest.mark.skip("Skip until we sort out why this is matching incorrectly")
def test_digest_gets_project_from_database(INMEMORY_SQLITE3):
    "Get data for a single project from database."
    # P1 Q1 asserts
    qtr_id = 1
    pjt_id = 1
    template = BICCTemplate(BICC_RETURN_MOCK, False)
    datamap = Datamap(template, INMEMORY_SQLITE3)
    datamap.cell_map_from_database()
    digest = Digest(datamap, qtr_id, pjt_id)
    digest.read_project_data()
    print()
    print(digest.data[0])
    print(digest.data[1])
    print(digest.data[2])
    print(digest.data[3])
    assert digest.data[0].cell_key == 'Project/Programme Name'
    assert digest.data[0].cell_value[
        0] == 'P1 Q1 DM1'
    assert digest.data[1].cell_value[0] == 'P1 Q1 DM2'
    assert digest.data[2].cell_value[0] == 'P1 Q1 DM3'
    # P1 Q2 asserts
    qtr_id = 2
    pjt_id = 1
    template = BICCTemplate(BICC_RETURN_MOCK, False)
    datamap = Datamap(template, INMEMORY_SQLITE3)
    datamap.cell_map_from_database()
    digest = Digest(datamap, qtr_id, pjt_id)
    digest.read_project_data()
    print()
    print(digest.data[0])
    print(digest.data[1])
    print(digest.data[2])
    print(digest.data[3])
    assert digest.data[0].cell_value[
        0] == 'P1 Q2 DM1'
    assert digest.data[1].cell_value[0] == 'P1 Q2 DM2'
    assert digest.data[2].cell_value[0] == 'P1 Q2 DM3'

    # P2 Q1 asserts
    qtr_id = 1
    pjt_id = 2
    template = BICCTemplate(BICC_RETURN_MOCK, False)
    datamap = Datamap(template, INMEMORY_SQLITE3)
    datamap.cell_map_from_database()
    digest = Digest(datamap, qtr_id, pjt_id)
    digest.read_project_data()
    print()
    print(digest.data[0])
    print(digest.data[1])
    print(digest.data[2])
    print(digest.data[3])
    assert digest.data[0].cell_value[
        0] == 'P2 Q1 DM1'
    assert digest.data[1].cell_value[0] == 'P2 Q1 DM2'
    assert digest.data[2].cell_value[0] == 'P2 Q1 DM3'

    # P2 Q2 asserts
    qtr_id = 2
    pjt_id = 2
    template = BICCTemplate(BICC_RETURN_MOCK, False)
    datamap = Datamap(template, INMEMORY_SQLITE3)
    datamap.cell_map_from_database()
    digest = Digest(datamap, qtr_id, pjt_id)
    digest.read_project_data()
    print()
    print(digest.data[0])
    print(digest.data[1])
    print(digest.data[2])
    print(digest.data[3])
    assert digest.data[0].cell_value[0] == 'P2 Q2 DM1'
    assert digest.data[1].cell_value[0] == 'P2 Q2 DM2'
    assert digest.data[2].cell_value[0] == 'P2 Q2 DM3'


def test_digest_reads_return(BICC_RETURN_MOCK, DATAMAP_MOCK, INMEMORY_SQLITE3):
    template = BICCTemplate(BICC_RETURN_MOCK)
    datamap = Datamap(template, INMEMORY_SQLITE3)
    datamap.cell_map_from_csv(DATAMAP_MOCK)
    digest = Digest(datamap, None, None)
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


def test_missing_series_item(INMEMORY_SQLITE3):
    qtr_id = 10
    pjt_id = 1
    template = BICCTemplate(BICC_RETURN_MOCK, False)
    datamap = Datamap(template, INMEMORY_SQLITE3)
    datamap.cell_map_from_database()
    digest = Digest(datamap, qtr_id, pjt_id)
    with pytest.raises(SeriesItemNotFoundError):
        digest.read_project_data()


def test_missing_project(INMEMORY_SQLITE3):
    qtr_id = 1
    pjt_id = 1000
    template = BICCTemplate(BICC_RETURN_MOCK, False)
    datamap = Datamap(template, INMEMORY_SQLITE3)
    datamap.cell_map_from_database()
    digest = Digest(datamap, qtr_id, pjt_id)
    with pytest.raises(ProjectNotFoundError):
        digest.read_project_data()


def test_both_missing_series_item_project(INMEMORY_SQLITE3):
    """
    This should raise SeriesItemNotFoundError, despite the fact that both
    series_item and project ids are not present.
    """
    qtr_id = 1000
    pjt_id = 1000
    template = BICCTemplate(BICC_RETURN_MOCK, False)
    datamap = Datamap(template, INMEMORY_SQLITE3)
    datamap.cell_map_from_database()
    digest = Digest(datamap, qtr_id, pjt_id)
    with pytest.raises(SeriesItemNotFoundError):
        digest.read_project_data()


# TODO - Test failing as read_project_data() called in Digest is connecting
# to generic Base db, not that owned by Datamap. Fixtures should override
# declarative base with their own model if tests are to be optimal.
@pytest.mark.skip("SEE TODO NOTE ABOVE FUNCTION")
def test_populate_blank_form_export_new(INMEMORY_SQLITE3, TEST_BLANK_XLS):
    qtr_id = 1
    pjt_id = 2
    import pudb; pudb.set_trace()  # XXX BREAKPOINT
    template = BICCTemplate(TEST_BLANK_XLS, True)
    datamap = Datamap(template, INMEMORY_SQLITE3)
    datamap.cell_map_from_database()
    digest = Digest(datamap, qtr_id, pjt_id)
    output_path = digest.write_to_template(TMP_DIR)
    wb = load_workbook(output_path)
    summary_sheet = wb['Summary']
    assert summary_sheet['A5'].value == 'P2 Q1 DM1'


def test_populate_blank_form_non_existing_qtr_proj_combo(INMEMORY_SQLITE3,
                                                         TEST_BLANK_XLS):
    qtr_id = 3
    pjt_id = 2
    template = BICCTemplate(TEST_BLANK_XLS, True)
    datamap = Datamap(template, INMEMORY_SQLITE3)
    datamap.cell_map_from_database()
    digest = Digest(datamap, qtr_id, pjt_id)
    with pytest.raises(NonExistantReturnError):
        digest.write_to_template(TMP_DIR)


def test_duplicate_record_on_write_to_db(INMEMORY_SQLITE3, BICC_RETURN_MOCK):
    qtr_id = 1
    pjt_id = 1
    template = BICCTemplate(BICC_RETURN_MOCK, False)
    datamap = Datamap(template, INMEMORY_SQLITE3)
    datamap.cell_map_from_database()
    digest = Digest(datamap, qtr_id, pjt_id)
    digest.read_template()
    with pytest.raises(DuplicateReturnError):
        digest.write_to_database()


def test_successful_write_return_to_db(INMEMORY_SQLITE3, BICC_RETURN_MOCK):
    conn = sqlite3.connect(INMEMORY_SQLITE3)
    c = conn.cursor()
    c.execute("DELETE FROM returns")
    conn.commit()
    qtr_id = 1
    pjt_id = 1
    template = BICCTemplate(BICC_RETURN_MOCK, False)
    datamap = Datamap(template, INMEMORY_SQLITE3)
    datamap.cell_map_from_database()
    digest = Digest(datamap, qtr_id, pjt_id)
    digest.read_template()
    digest._get_existing_return_project_and_series_item_ids()
    digest.write_to_database()
    test_returns = c.execute("SELECT value FROM returns").fetchone()
    conn.commit()
    conn.close()
    assert test_returns[0] == "Project/Programme Name"


def test_attempt_to_write_return_to_db_unavailable_qtr(INMEMORY_SQLITE3,
                                                       BICC_RETURN_MOCK):
    qtr_id = 100
    pjt_id = 1
    template = BICCTemplate(BICC_RETURN_MOCK, False)
    datamap = Datamap(template, INMEMORY_SQLITE3)
    datamap.cell_map_from_database()
    digest = Digest(datamap, qtr_id, pjt_id)
    digest.read_template()
    with pytest.raises(SeriesItemNotFoundError):
        digest.write_to_database()


def test_attempt_to_write_return_to_db_unavailable_project(INMEMORY_SQLITE3,
                                                           BICC_RETURN_MOCK):
    qtr_id = 1
    pjt_id = 100
    template = BICCTemplate(BICC_RETURN_MOCK, False)
    datamap = Datamap(template, INMEMORY_SQLITE3)
    datamap.cell_map_from_database()
    digest = Digest(datamap, qtr_id, pjt_id)
    digest.read_template()
    with pytest.raises(ProjectNotFoundError):
        digest.write_to_database()


def test_file_name_cleaner(INMEMORY_SQLITE3, BICC_RETURN_MOCK):
    qtr_id = 1
    pjt_id = 1
    template = BICCTemplate(BICC_RETURN_MOCK, False)
    datamap = Datamap(template, INMEMORY_SQLITE3)
    datamap.cell_map_from_database()
    digest = Digest(datamap, qtr_id, pjt_id)
    digest.read_template()
    assert digest._generate_file_name_from_return_data(
        qtr_id, pjt_id) == 'Project_1_Q1_2013_14'


def test_get_project_name_from_digest(INMEMORY_SQLITE3, BICC_RETURN_MOCK):
    qtr_id = 1
    pjt_id = 1
    template = BICCTemplate(BICC_RETURN_MOCK, False)
    datamap = Datamap(template, INMEMORY_SQLITE3)
    datamap.cell_map_from_database()
    digest = Digest(datamap, qtr_id, pjt_id)
    assert digest.project_name == "Project 1"
