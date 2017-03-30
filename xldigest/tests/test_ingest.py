from xldigest.process.template import BICCTemplate
from xldigest.process.datamap import Datamap
from xldigest.process.digest import Digest
from xldigest.process.ingestor import Ingestor
from xldigest.process.exceptions import (QuarterNotFoundError,
                                         ProjectNotFoundError,
                                         DuplicateReturnError,
                                         NonExistantReturnError)

from openpyxl import load_workbook

import xldigest.tests.fixtures as fixtures
import pytest
import sqlite3


BICC_RETURN_MOCK = fixtures.bicc_return
DATAMAP_MOCK = fixtures.mock_datamap_source_file
INMEMORY_SQLITE3 = fixtures.sqlite3_db_file
TEST_BLANK_XLS = fixtures.test_blank_xls


def test_ingestor_obect():
    ingestor = Ingestor()
    assert ingestor.__str__() == "Ingestor()"
