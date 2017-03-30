import os

from xldigest.process.template import BICCTemplate
from xldigest.process.datamap import Datamap
from xldigest.process.digest import Digest
from xldigest.process.ingestor import Ingestor
from xldigest.process.exceptions import (QuarterNotFoundError,
                                         ProjectNotFoundError,
                                         DuplicateReturnError,
                                         NonExistantReturnError)

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


def test_ingestor_source_dir_contains_xls_files():
    ingestor = Ingestor(SOURCE_DIR, PORTFOLIO, SERIES, SERIES_ITEM)
    mock_blank_xlsx_file(SOURCE_DIR)
    is_there_files = ingestor.source_xls_only()
    assert is_there_files is True
