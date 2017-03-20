from xldigest.process.template import BICCTemplate
from xldigest.process.datamap import Datamap
from xldigest.process.digest import Digest
from xldigest.process.exceptions import (QuarterNotFoundError,
                                         ProjectNotFoundError)
import xldigest.tests.fixtures as fixtures
import pytest
import sqlite3

BICC_RETURN_MOCK = fixtures.bicc_return
DATAMAP_MOCK = fixtures.mock_datamap_source_file
INMEMORY_SQLITE3 = fixtures.sqlite3_db_file


def test_in_tmp_sqlite3(INMEMORY_SQLITE3):
    conn = sqlite3.connect(INMEMORY_SQLITE3)
    c = conn.cursor()
    q1 = c.execute("SELECT * FROM quarters").fetchone()[1]
    p1 = c.execute("SELECT * FROM projects").fetchone()[1]
    assert q1 == "Q1 2016/17"
    assert p1 == "Project 1"


def test_digest_gets_datamap(BICC_RETURN_MOCK, DATAMAP_MOCK, INMEMORY_SQLITE3):
    """Uses import_csv() function to process the datamap text file."""
    template = BICCTemplate(BICC_RETURN_MOCK)
    datamap = Datamap(template,
                      INMEMORY_SQLITE3)
    datamap.import_csv(DATAMAP_MOCK)
    digest = Digest(datamap, None, None)
    assert digest.datamap.cell_map[0].cell_key == 'Project/Programme Name'
    assert digest.datamap.cell_map[2].cell_key == 'GMPP - FD Sign-Off'


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
    datamap.import_csv(DATAMAP_MOCK)
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


def test_missing_quarter(INMEMORY_SQLITE3):
    qtr_id = 10
    pjt_id = 1
    template = BICCTemplate(BICC_RETURN_MOCK, False)
    datamap = Datamap(template, INMEMORY_SQLITE3)
    datamap.cell_map_from_database()
    digest = Digest(datamap, qtr_id, pjt_id)
    with pytest.raises(QuarterNotFoundError):
        # TODO Need to work on this Exception test
        digest.read_project_data()


def test_missing_project(INMEMORY_SQLITE3):
    qtr_id = 1
    pjt_id = 1000
    template = BICCTemplate(BICC_RETURN_MOCK, False)
    datamap = Datamap(template, INMEMORY_SQLITE3)
    datamap.cell_map_from_database()
    digest = Digest(datamap, qtr_id, pjt_id)
    with pytest.raises(ProjectNotFoundError):
        # TODO Need to work on this Exception test
        digest.read_project_data()
