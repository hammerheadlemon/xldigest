import argparse
import csv
from datetime import date

import os

from xldigest import Session
from xldigest.database.models import (DatamapItem, Project, Portfolio,
                                      ReturnItem, Series, SeriesItem)
from xldigest.process.datamap import Datamap
from xldigest.process.digest import Digest
from xldigest.process.template import BICCTemplate

# Hard-coded for now - this matches the current quarter with the same
# value in the database so we're not relying on how it's written in
# BICC template.
# CURRENT_QUARTER = "Q3 2016/17"
CURRENT_QUARTER = None


def _change_dict_val(target, replacement, dictionary):
    """Helper script to strip or change values in a dict."""
    for k, v in dictionary.items():
        if v == target:
            dictionary[k] = replacement
    return dictionary


def _strip_trailing_whitespace(dictionary):
    """Helper script to strip trailing whitespace from string values in dict."""
    for k, v in dictionary.items():
        # probably a string
        if isinstance(v, str):
            dictionary[k] = v.rstrip()
    return dictionary


def import_datamap_csv(source_file, session: Session):
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


def merge_gmpp_datamap(source_file, session: Session):
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


def populate_series_table(series_name, session: Session) -> None:
    """
    A single series: Financial Quarters
    """
    session.add(Series(name=series_name))
    session.commit()


def populate_series_item_table(session: Session, series_items: list):
    """
    Populate basic Quarter information as SeriesItem objects.
    """
    #  1
    for series_item in series_items:
        session.add(
            SeriesItem(
                name=series_item,
                series=1,
                start_date=date(2012, 4, 1),
                end_date=date(2012, 6, 30)))
    session.commit()


def populate_portfolio_table(portfolio_name, session: Session) -> None:
    """
    Populate the Portfolio table.
    """
    session.add(Portfolio(name=portfolio_name))
    session.commit()


def populate_projects_table(portfolio_id: int, session: Session) -> None:
    """
    Populate the project table in the database. The master_transposed.csv
    file is used as the source for this.
    
    WILL BE REDUNDANT WHEN GUI COMPLETE.
    """
    with open('/home/lemon/Documents/xldigest/source/master_transposed.csv'
              ) as f:
        reader = csv.DictReader(f)
        project_list = [row['Project/Programme Name'] for row in reader]
        for p in project_list:
            p = Project(name=p, portfolio=portfolio_id)
            session.add(p)
        session.commit()


def populate_projects_table_from_gui(portfolio_id: int, projects_list: list, session: Session) -> None:
    for p in projects_list:
        p = Project(name=p, portfolio=portfolio_id)
        session.add(p)
    session.commit()


def _query_for_single_project_id(prj_str: str, session: Session) -> int:
    project_id = session.query(Project.id).filter(
        Project.name == prj_str).first()[0]
    return project_id


def import_single_bicc_return_using_database(source_file: str,
                                             series_item_id: int,
                                             project_id: int,
                                             session: Session) -> None:
    """
    Import a single BICC return based on a source template. Use the datamap
    from database, rather than the csv file.
    """
    # we need the project_id to build the tables
    # TODO finish this function - prj_str used here needs to be passed
    # to this function by the calling loop

    template = BICCTemplate(source_file)

    datamap = Datamap(template)
    datamap.cell_map_from_database()
    digest = Digest(datamap, series_item_id, project_id, session)
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


def import_all_returns_to_database(series_item: str, session: Session) -> None:
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
            os.path.join(returns_dir, f), quarter_id, 1, session)


def main():
    session = Session()
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i",
        "--initial",
        help="Creates all the necessary tables. Run first",
        action="store_true")
    parser.add_argument(
        "-s",
        "--secondary",
        help=
        "Imports returns. You must include a suitable string for which the series item, e.g 'Q4 2014/15'",
        nargs=1,
        metavar="QUARTER")
    parser.parse_args()
    args = parser.parse_args()
    if args.initial:
        import_datamap_csv('/home/lemon/Documents/xldigest/source/'
                           'datamap-returns-to-master-WITH_HEADER_FORSQLITE', session)
        merge_gmpp_datamap('/home/lemon/Documents/xldigest/source/'
                           'datamap-master-to-gmpp', session)
        populate_portfolio_table("DfT Tier 1 Projects", session)
        populate_series_table("Financial Quarters", session)
        populate_projects_table(1, session)
        populate_series_item_table(['Q1 2017/18', 'Q2 2017/18', 'Q3 2017/18'
                                                                'Q4 2017/18'])
    elif args.secondary:
        CURRENT_QUARTER = args.secondary[0]
        import_all_returns_to_database(CURRENT_QUARTER, session)


if __name__ == "__main__":
    main()
