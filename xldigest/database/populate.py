import argparse
import csv
import os

from datetime import date

from xldigest.database.setup import set_up_session, USER_DATA_DIR
from xldigest.process.datamap import Datamap
from xldigest.process.digest import Digest
from xldigest.process.template import BICCTemplate

from xldigest.database.models import (DatamapItem, Project, Portfolio,
                                      ReturnItem, Series, SeriesItem)


db_pth = os.path.join(USER_DATA_DIR, 'db.sqlite')
print(db_pth)
session = set_up_session(db_pth)

# Hard-coded for now - this matches the current quarter with the same
# value in the database so we're not relying on how it's written in
# BICC template.
CURRENT_QUARTER = "Q3 2016/17"


def _change_dict_val(target, replacement, dictionary):
    "Helper script to strip or change values in a dict."
    for k, v in dictionary.items():
        if v == target:
            dictionary[k] = replacement
    return dictionary


def _strip_trailing_whitespace(dictionary):
    "Helper script to strip trailing whitespace from string values in dict."
    for k, v in dictionary.items():
        # probably a string
        if isinstance(v, str):
            dictionary[k] = v.rstrip()
    return dictionary


def import_datamap_csv(source_file):
    """
    Import a csv-based datamap into a sqlite database.
    """

    with open(source_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            row = _change_dict_val("", None, row)
            row = _strip_trailing_whitespace(row)
            dmi = DatamapItem(
                key=row['key'],
                bicc_sheet=row['bicc_sheet'],
                bicc_cellref=row['bicc_cellref'],
                bicc_ver_form=row['bicc_verification_formula'])
            session.add(dmi)

        session.commit()
        session.close()


def merge_gmpp_datamap(source_file):
    """
    Merge-in relevant cell references from a GMPP-based datamap, based on
    values from the returns-to-master datamap.
    """
    keys = [instance.key for instance in session.query(DatamapItem)]

    with open(source_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            row = _change_dict_val("", None, row)
            row = _strip_trailing_whitespace(row)
            if row['master_cellname'] in keys:
                target_instance = session.query(DatamapItem).filter_by(
                    key=row['master_cellname']).first()
                target_instance.gmpp_sheet = row[
                    'gmpp_template_sheet_reference']
                target_instance.gmpp_cellref = row[
                    'gmpp_template_cell_reference']
    session.commit()


def populate_series_table() -> None:
    """
    A single series: Financial Quarters
    """
    session.add(Series(name='Financial Quarters'))
    session.commit()


def populate_quarters_table():
    """
    Populate basic Quarter information as SeriesItem objects.
    """
    #  1
    session.add(
        SeriesItem(
            name='Q1 2012/13',
            series=1,
            start_date=date(2012, 4, 1),
            end_date=date(2012, 6, 30)))
    session.add(
        SeriesItem(
            name='Q2 2012/13',
            series=1,
            start_date=date(2012, 7, 1),
            end_date=date(2012, 9, 30)))
    session.add(
        SeriesItem(
            name='Q3 2012/13',
            series=1,
            start_date=date(2012, 10, 1),
            end_date=date(2012, 12, 31)))
    session.add(
        SeriesItem(
            name='Q4 2012/13',
            series=1,
            start_date=date(2013, 1, 1),
            end_date=date(2013, 3, 31)))

    #  2
    session.add(
        SeriesItem(
            name='Q1 2013/14',
            series=1,
            start_date=date(2013, 4, 1),
            end_date=date(2013, 6, 30)))
    session.add(
        SeriesItem(
            name='Q2 2013/14',
            series=1,
            start_date=date(2013, 7, 1),
            end_date=date(2013, 9, 30)))
    session.add(
        SeriesItem(
            name='Q3 2013/14',
            series=1,
            start_date=date(2013, 10, 1),
            end_date=date(2013, 12, 31)))
    session.add(
        SeriesItem(
            name='Q4 2013/14',
            series=1,
            start_date=date(2014, 1, 1),
            end_date=date(2014, 3, 31)))

    #  3
    session.add(
        SeriesItem(
            name='Q1 2014/15',
            series=1,
            start_date=date(2014, 4, 1),
            end_date=date(2014, 6, 30)))
    session.add(
        SeriesItem(
            name='Q2 2014/15',
            series=1,
            start_date=date(2014, 7, 1),
            end_date=date(2014, 9, 30)))
    session.add(
        SeriesItem(
            name='Q3 2014/15',
            series=1,
            start_date=date(2014, 10, 1),
            end_date=date(2014, 12, 31)))
    session.add(
        SeriesItem(
            name='Q4 2014/15',
            series=1,
            start_date=date(2015, 1, 1),
            end_date=date(2015, 3, 31)))

    #  4
    session.add(
        SeriesItem(
            name='Q1 2015/16',
            series=1,
            start_date=date(2015, 4, 1),
            end_date=date(2015, 6, 30)))
    session.add(
        SeriesItem(
            name='Q2 2015/16',
            series=1,
            start_date=date(2015, 7, 1),
            end_date=date(2015, 9, 30)))
    session.add(
        SeriesItem(
            name='Q3 2015/16',
            series=1,
            start_date=date(2015, 10, 1),
            end_date=date(2015, 12, 31)))
    session.add(
        SeriesItem(
            name='Q4 2015/16',
            series=1,
            start_date=date(2016, 1, 1),
            end_date=date(2016, 3, 31)))

    #  5
    session.add(
        SeriesItem(
            name='Q1 2016/17',
            series=1,
            start_date=date(2016, 4, 1),
            end_date=date(2016, 6, 30)))
    session.add(
        SeriesItem(
            name='Q2 2016/17',
            series=1,
            start_date=date(2016, 7, 1),
            end_date=date(2016, 9, 30)))
    session.add(
        SeriesItem(
            name='Q3 2016/17',
            series=1,
            start_date=date(2016, 10, 1),
            end_date=date(2016, 12, 31)))
    session.add(
        SeriesItem(
            name='Q4 2016/17',
            series=1,
            start_date=date(2017, 1, 1),
            end_date=date(2017, 3, 31)))

    #  6
    session.add(
        SeriesItem(
            name='Q1 2017/18',
            series=1,
            start_date=date(2017, 4, 1),
            end_date=date(2017, 6, 30)))
    session.add(
        SeriesItem(
            name='Q2 2017/18',
            series=1,
            start_date=date(2017, 7, 1),
            end_date=date(2017, 9, 30)))
    session.add(
        SeriesItem(
            name='Q3 2017/18',
            series=1,
            start_date=date(2017, 10, 1),
            end_date=date(2017, 12, 31)))
    session.add(
        SeriesItem(
            name='Q4 2017/18',
            series=1,
            start_date=date(2018, 1, 1),
            end_date=date(2018, 3, 31)))

    #  7
    session.add(
        SeriesItem(
            name='Q1 2018/19',
            series=1,
            start_date=date(2018, 4, 1),
            end_date=date(2018, 6, 30)))
    session.add(
        SeriesItem(
            name='Q2 2018/19',
            series=1,
            start_date=date(2018, 7, 1),
            end_date=date(2018, 9, 30)))
    session.add(
        SeriesItem(
            name='Q3 2018/19',
            series=1,
            start_date=date(2018, 10, 1),
            end_date=date(2018, 12, 31)))
    session.add(
        SeriesItem(
            name='Q4 2018/19',
            series=1,
            start_date=date(2019, 1, 1),
            end_date=date(2019, 3, 31)))

    #  8
    session.add(
        SeriesItem(
            name='Q1 2019/20',
            series=1,
            start_date=date(2019, 4, 1),
            end_date=date(2019, 6, 30)))
    session.add(
        SeriesItem(
            name='Q2 2019/20',
            series=1,
            start_date=date(2019, 7, 1),
            end_date=date(2019, 9, 30)))
    session.add(
        SeriesItem(
            name='Q3 2019/20',
            series=1,
            start_date=date(2019, 10, 1),
            end_date=date(2019, 12, 31)))
    session.add(
        SeriesItem(
            name='Q4 2019/20',
            series=1,
            start_date=date(2020, 1, 1),
            end_date=date(2020, 3, 31)))
    session.commit()


def populate_portfolio_table() -> None:
    """
    Populate the Portfolio table.
    """
    session.add(Portfolio(name="DfT Tier 1 Projects Portfolio"))
    session.commit()


def populate_projects_table(portfolio_id: int) -> None:
    """
    Populate the project table in the database. The master_transposed.csv
    file is used as the source for this.
    """
    with open('/home/lemon/Documents/xldigest/source/master_transposed.csv'
              ) as f:
        reader = csv.DictReader(f)
        project_list = [row['Project/Programme Name'] for row in reader]
        for p in project_list:
            p = Project(name=p, portfolio=1)
            session.add(p)
    session.commit()


def _query_for_single_project_id(prj_str: str) -> int:
    project_id = session.query(Project.id).filter(
        Project.name == prj_str).first()[0]
    return project_id


def import_single_bicc_return_using_database(source_file: str,
                                             series_item_id: int,
                                             project_id: int) -> None:
    """
    Import a single BICC return based on a source template. Use the datamap
    from database, rather than the csv file.
    """
    # we need the project_id to build the tables
    # TODO finish this function - prj_str used here needs to be passed
    # to this function by the calling loop

    template = BICCTemplate(source_file)

    datamap = Datamap(template,
                      '{}{}'.format(USER_DATA_DIR, '/db.sqlite'))
    datamap.cell_map_from_database()
    digest = Digest(datamap, series_item_id, project_id)
    digest.read_template()

    project_name = [
        item.cell_value.rstrip() for item in datamap.cell_map
        if item.cell_key == 'Project/Programme Name'
    ]

    # we need project_id to build the tables
    try:
        project_id = session.query(Project.id).filter(
            Project.name == project_name[0]).all()[0][0]
    except IndexError:
        print("Project {} not in projects table. Fix it!".format(project_name))
        project_id = None

    # go through the cell_map in the Digest object and drop into database
    for cell in digest.data:

        cell_val_id = session.query(DatamapItem.id).filter(
            DatamapItem.key == cell.cell_key).all()[0][0]

        return_item = ReturnItem(
            project_id=project_id,
            series_item_id=series_item_id,
            datamap_item_id=cell_val_id,
            value=cell.cell_value)
        session.add(return_item)
    session.commit()


def import_all_returns_to_database(series_item: str) -> None:
    """
    Runs through a directory of files and calls
    import_single_bicc_return_using_database on each one. Does not distinguish
    between xlsx files and not so ensure no extraenneous files in there.
    """
    returns_dir = os.path.dirname('/home/lemon/Documents/xldigest/source/'
                                  'returns/')
    quarter_id = session.query(SeriesItem.id).filter(
        SeriesItem.name == series_item).all()[0][0]
    for f in os.listdir(returns_dir):
        print("Importing {}".format(f))
        import_single_bicc_return_using_database(
            os.path.join(returns_dir, f), quarter_id, 1)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i",
        "--initial",
        help="Creates all the necessary tables. Run first",
        action="store_true")
    parser.add_argument(
        "-s",
        "--secondary",
        help="Imports returns",
        action="store_true")
    parser.parse_args()
    args = parser.parse_args()
    if args.initial:
        import_datamap_csv('/home/lemon/Documents/xldigest/source/'
                           'datamap-returns-to-master-WITH_HEADER_FORSQLITE')
        merge_gmpp_datamap('/home/lemon/Documents/xldigest/source/'
                           'datamap-master-to-gmpp')
        populate_portfolio_table()
        populate_series_table()
        populate_projects_table(1)
        populate_quarters_table()
    elif args.secondary:
        import_all_returns_to_database(CURRENT_QUARTER)


if __name__ == "__main__":
    main()
