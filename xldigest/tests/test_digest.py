from xldigest.process.template import BICCTemplate
from xldigest.process.datamap import Datamap
from xldigest.process.digest import Digest
import xldigest.tests.fixtures as fixtures

BICC_RETURN_MOCK = fixtures.bicc_return
DATAMAP_MOCK = fixtures.mock_datamap_source_file


def test_digest_gets_datamap(BICC_RETURN_MOCK, DATAMAP_MOCK):
    """Uses import_csv() function to process the datamap text file."""
    template = BICCTemplate(BICC_RETURN_MOCK)
    datamap = Datamap(template, '/home/lemon/code/python/xldigest/xldigest/db.sqlite')
    datamap.import_csv(DATAMAP_MOCK)
    digest = Digest(datamap, None)
    assert digest.datamap.cell_map[0].cell_key == 'Project/Programme Name'
    assert digest.datamap.cell_map[2].cell_key == 'GMPP - FD Sign-Off'


def test_digest_gets_project_from_database():
    "Get data for a single project from database."
    template = BICCTemplate(BICC_RETURN_MOCK, False)
    datamap = Datamap(template, '/home/lemon/code/python/xldigest/xldigest/db.sqlite')
    datamap.cell_map_from_database()
    digest = Digest(datamap, 1)
    digest.read_project_data(1, 1)
    print(digest.data)


def test_digest_reads_return(BICC_RETURN_MOCK, DATAMAP_MOCK):
    template = BICCTemplate(BICC_RETURN_MOCK)
    datamap = Datamap(template, '/home/lemon/code/python/xldigest/xldigest/db.sqlite')
    datamap.import_csv(DATAMAP_MOCK)
    digest = Digest(datamap, None)
    # here we need to go through the datamap, use the cell_key and
    # cell_reference to populate the cell_value of the Cell object
    digest.read_template()
    print("\n")
    for cell in digest.data:
        try:
            print("{0:<70}{1:<30}{2:<70}".format(
                cell.cell_key,
                cell.template_sheet,
                cell.cell_value))
        except Exception:
            pass
    # WARNING: digest.data[] index here depends on whether the cell_reference
    # is not None. Cell objects whose cell_reference value is None
    # will NOT be migrated into the Digest object, therefore the order of
    # Cell objects in the .data member will vary depending on the Datamap.
    assert digest.data[0].cell_value == 'Cookfield Rebuild'
    assert digest.data[0].cell_reference == 'B5'
    assert digest.data[0].template_sheet == 'Summary'
    assert digest.data[4].cell_value == 2012
