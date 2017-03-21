import csv
import pytest

from xldigest.process.datamap import Datamap
from xldigest.process.cell import Cell
from xldigest.process.template import BICCTemplate


@pytest.fixture
def mock_datamap_source_file():
    data = [
        ['Project/Programme Name', 'Summary', 'B5'],
        ['GMPP - Classification', 'Official-Sensitive'],
        ['SRO Sign-Off', 'Summary', 'B49'],
        ['GMPP - FD Sign-Off', 'Summary'],
        ['GMPP - Person completing this return'],
        ['GMPP - Single Point of Contact Email Address'],
        ['GMPP - Single Point of Contact (SPOC)'],
        ['GMPP - Email Address'],
        ['Reporting period (GMPP - Snapshot Date)', 'Summary', 'G3'],
        ['Quarter Joined', 'Summary', 'I3'],
        ['GMPP - Sub-portfolio'],
        ['GMPP/quarter formally joined'],
        ['GMPP (GMPP – formally joined GMPP)', 'Summary', 'G5'],
        ['IUK top 40', 'Summary', 'G6'],
        ['Top 37', 'Summary', 'I5'],
        ['DfT Business Plan', 'Summary', 'I6'],
        ['GMPP - IPA ID Number', 'Summary', 'C6'],
        ['DFT ID Number', 'Summary', 'B6'],
        ['Working Contact Name', 'Summary', 'H8'],
        ['Working Contact Telephone', 'Summary', 'H9', 'red', '', 'd/mm/yy'],
        ['Working Contact Email', 'Summary', 'H10'],
        [
            'Significant Steel Requirement', 'Finance & Benefits', 'D15',
            'Yes/No'
        ],
        ['SRO Finance confidence', 'Finance & Benefits', 'C6', 'RAG_Short'],
        ['BICC approval point', 'Finance & Benefits', 'E9', 'Business Cases'],
    ]
    with open('/tmp/mock_datamap.csv', 'w') as f:
        datamap_writer = csv.writer(f, delimiter=',')
        f.write('cell_key,template_sheet,cell_reference,bg_colour,fg_colour'
                ',number_format,verification_list\n')
        for item in data:
            datamap_writer.writerow(item)
    return '/tmp/mock_datamap.csv'


def test_for_datamap_class():
    template = BICCTemplate('tmp/bicc_template.xlsx')
    datamap = Datamap(template, '/home/lemon/code/python/xldigest/xldigest/db.sqlite')
    assert datamap


def test_expect_datamap_cell():
    template = BICCTemplate('tmp/bicc_template.xlsx')
    sheet = template.add_sheet('Summary')
    datamap = Datamap(template, '/home/lemon/code/python/xldigest/xldigest/db.sqlite')
    cell = Cell(
            datamap_id=None,
            cell_key='Project/Programme Name',
            cell_value=None,
            cell_reference='B5',
            template_sheet=sheet,
            bg_colour=None,
            fg_colour=None,
            number_format=None,
            verification_list=None
            )
    assert datamap.add_cell(cell)


def test_datamap_source_file(mock_datamap_source_file):
    template = BICCTemplate('/tmp/bicc_template.xlsx')
    datamap = Datamap(template, '/home/lemon/code/python/xldigest/xldigest/db.sqlite')
    datamap.cell_map_from_csv(mock_datamap_source_file)
    assert isinstance(datamap.cell_map[0], Cell)
    assert datamap.cell_map[0].cell_key == 'Project/Programme Name'
    assert datamap.cell_map[5].template_sheet is None
    assert datamap.cell_map[19].number_format == 'd/mm/yy'
