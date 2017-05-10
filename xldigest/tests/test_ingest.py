import getpass
import platform

import xldigest.database.paths

from xldigest.process.ingestor import Ingestor
from xldigest.process.exceptions import (NoFilesInDirectoryError,
                                         DuplicateReturnError)

from xldigest.process.template import BICCTemplate

from xldigest.tests.fixtures import mock_blank_xlsx_file, TMP_DIR

import xldigest.tests.fixtures as fixtures
import os
import pytest
import sqlite3

from openpyxl import load_workbook

BICC_RETURN_MOCK = fixtures.bicc_return
DATAMAP_MOCK = fixtures.mock_datamap_source_file
INMEMORY_SQLITE3 = fixtures.sqlite3_db_file
SOURCE_DIR = os.path.join(TMP_DIR, 'xlsx_tests/')
PORTFOLIO = 1
SERIES = 1
SERIES_ITEM = 1


def test_ingestor_object():
    ingestor = Ingestor(INMEMORY_SQLITE3, SOURCE_DIR, PORTFOLIO, SERIES, SERIES_ITEM)
    assert ingestor.__str__() == "Ingestor()"


def test_ingestor_source_dir():
    ingestor = Ingestor(INMEMORY_SQLITE3, SOURCE_DIR, PORTFOLIO, SERIES, SERIES_ITEM)
    assert ingestor.source_dir == SOURCE_DIR


def test_ingestor_source_dir_contains_only_xls_files():
    ingestor = Ingestor(INMEMORY_SQLITE3, SOURCE_DIR, PORTFOLIO, SERIES, SERIES_ITEM)
    mock_blank_xlsx_file(SOURCE_DIR)
    is_there_files = ingestor.source_xls_only()
    assert is_there_files is True


def test_ingestor_source_dir_contains_mixed_files():
    ingestor = Ingestor(INMEMORY_SQLITE3, SOURCE_DIR, PORTFOLIO, SERIES, SERIES_ITEM)
    mock_blank_xlsx_file(SOURCE_DIR, mix=True)
    is_there_files = ingestor.source_xls_only()
    assert is_there_files is False


def test_ingestor_source_dir_contains_no_files():
    ingestor = Ingestor(INMEMORY_SQLITE3, SOURCE_DIR, PORTFOLIO, SERIES, SERIES_ITEM)
    mock_blank_xlsx_file(SOURCE_DIR, empty=True)
    with pytest.raises(NoFilesInDirectoryError):
        ingestor.source_xls_only()


def test_series_object(INMEMORY_SQLITE3):
    conn = sqlite3.connect(INMEMORY_SQLITE3)
    c = conn.cursor()
    series = c.execute("SELECT * FROM series").fetchone()[1]
    assert series == 'Financial Quarters'


def test_series_item_object(INMEMORY_SQLITE3):
    conn = sqlite3.connect(INMEMORY_SQLITE3)
    c = conn.cursor()
    series_item = c.execute("SELECT * FROM series_items").fetchone()
    assert series_item[1] == 'Q1 2013/14'
    assert series_item[0] == 1
    assert series_item[2] == '2013-04-01'
    assert series_item[3] == '2013-06-30'


def test_application_data_path():
    usr = getpass.getuser()
    if platform.system() == 'Linux':
        assert xldigest.database.paths.USER_DATA_DIR == '/home/{}/.local/share/{}'.format(usr, xldigest.database.paths.APPNAME)
    elif platform.system() == 'Windows':
        assert xldigest.database.paths.USER_DATA_DIR == 'C:\\Users\\{}\\AppData\\Local\\{}\\{}'.format(
            usr, xldigest.database.paths.APPAUTHOR, xldigest.database.paths.APPNAME)


def test_import_save_and_uuid_alloc(INMEMORY_SQLITE3, BICC_RETURN_MOCK):
    source_template = BICCTemplate(BICC_RETURN_MOCK)
    ingestor = Ingestor(
        INMEMORY_SQLITE3,
        project_id=1,
        portfolio_id=1,
        series_item_id=1,
        source_file=source_template)
    saved_file = ingestor.write_source_file()
    if saved_file != "":
        f = load_workbook(saved_file)
        assert f['Summary']['A5'].value == 'Project/Programme Name'


def test_import_duplicate_return(INMEMORY_SQLITE3, BICC_RETURN_MOCK):
    source_template = BICCTemplate(BICC_RETURN_MOCK)
    ingestor = Ingestor(
        INMEMORY_SQLITE3,
        project_id=1,
        portfolio_id=1,
        series_item_id=1,
        source_file=source_template)
    with pytest.raises(DuplicateReturnError):
        saved_file = ingestor.write_source_file()


def test_import_single_return_using_ingestor(INMEMORY_SQLITE3, BICC_RETURN_MOCK):
    source_template = BICCTemplate(BICC_RETURN_MOCK)
    ingestor = Ingestor(
        INMEMORY_SQLITE3,
        project_id=1,
        portfolio_id=1,
        series_item_id=1,
        source_file=source_template)
    saved_file = ingestor.write_source_file()
    ingestor.import_single_return()
    conn = sqlite3.connect(INMEMORY_SQLITE3)
    c = conn.cursor()
    return_item = c.execute("SELECT * FROM returns").fetchone()
    assert "1_1_1" in saved_file
    assert return_item == (1, 1, 1, 1, 'P1 Q1 DM1')
