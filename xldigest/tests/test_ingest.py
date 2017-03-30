import os

from xldigest.process.template import BICCTemplate
from xldigest.process.datamap import Datamap
from xldigest.process.digest import Digest
from xldigest.process.ingestor import Ingestor
from xldigest.process.exceptions import (QuarterNotFoundError,
                                         ProjectNotFoundError,
                                         DuplicateReturnError,
                                         NonExistantReturnError,
                                         NoFilesInDirectoryError)

from xldigest.tests.fixtures import mock_blank_xlsx_file

from openpyxl import load_workbook

import xldigest.tests.fixtures as fixtures
import pytest
import sqlite3


BICC_RETURN_MOCK = fixtures.bicc_return
DATAMAP_MOCK = fixtures.mock_datamap_source_file
INMEMORY_SQLITE3 = fixtures.sqlite3_db_file
SOURCE_DIR = '/tmp/xlsx_tests'
PORTFOLIO = 1
SERIES = 1
SERIES_ITEM = 1


def test_ingestor_obect():
    ingestor = Ingestor(SOURCE_DIR, PORTFOLIO, SERIES, SERIES_ITEM)
    assert ingestor.__str__() == "Ingestor()"


def test_ingestor_source_dir():
    ingestor = Ingestor(SOURCE_DIR, PORTFOLIO, SERIES, SERIES_ITEM)
    assert ingestor.source_dir == SOURCE_DIR


def test_ingestor_source_dir_contains_only_xls_files():
    ingestor = Ingestor(SOURCE_DIR, PORTFOLIO, SERIES, SERIES_ITEM)
    mock_blank_xlsx_file(SOURCE_DIR)
    is_there_files = ingestor.source_xls_only()
    assert is_there_files is True


def test_ingestor_source_dir_contains_mixed_files():
    ingestor = Ingestor(SOURCE_DIR, PORTFOLIO, SERIES, SERIES_ITEM)
    mock_blank_xlsx_file(SOURCE_DIR, mix=True)
    is_there_files = ingestor.source_xls_only()
    assert is_there_files is False


def test_ingestor_source_dir_contains_no_files():
    ingestor = Ingestor(SOURCE_DIR, PORTFOLIO, SERIES, SERIES_ITEM)
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
