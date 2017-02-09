import csv
import os
import sys
import sqlite3

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from xldigest.process.datamap import Datamap
from xldigest.process.digest import Digest
from xldigest.process.template import BICCTemplate

from xldigest.database.models import (DatamapItem, Project, Quarter, Base,
                                      ReturnItem)

engine = create_engine('sqlite:///db.sqlite')

Session = sessionmaker(bind=engine)

session = Session()

# Hard-coded for now - this matches the current quarter with the same
# value in the database so we're not relying on how it's written in
# BICC template.
CURRENT_QUARTER = "Q2 2016/17"


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


def populate_quarters_table():
    """
    Populate basic Quarter information.
    """
    session.add_all([
        Quarter(name='Q2 2016/17'), Quarter(name='Q3 2016/17'),
        Quarter(name='Q4 2016/17'), Quarter(name='Q1 2017/18'),
        Quarter(name='Q2 2017/18'), Quarter(name='Q3 2017/18'),
        Quarter(name='Q4 2017/18'), Quarter(name='Q1 2018/19'),
        Quarter(name='Q2 2018/19'), Quarter(name='Q3 2018/19'),
        Quarter(name='Q4 2018/19'), Quarter(name='Q5 2019/20')
    ])
    session.commit()


def populate_projects_table():
    """
    Populate the project table in the database. The master_transposed.csv
    file is used as the source for this.
    """
    with open('/home/lemon/Documents/bcompiler/source/master_transposed.csv'
              ) as f:
        reader = csv.DictReader(f)
        project_list = [row['Project/Programme Name'] for row in reader]
        for p in project_list:
            p = Project(name=p)
            session.add(p)
    session.commit()


def import_single_bicc_return_using_database(source_file):
    """
    Import a single BICC return based on a source template. Use the datamap
    from database, rather than the csv file.
    """
    template = BICCTemplate(source_file)
    datamap = Datamap(template,
                      '/home/lemon/code/python/xldigest/xldigest/db.sqlite')
    # call the bcompiler class here
    datamap.cell_map_from_database()
    digest = Digest(datamap)
    digest.read_template()

    # we need project_names to build the tables
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

    # we need quarter_id to build the tables
    quarter_id = session.query(Quarter.id).filter(
        Quarter.name == CURRENT_QUARTER).all()[0][0]

    # go through the cell_map in the Digest object and drop into database
    for cell in digest.data:

        cell_val_id = session.query(DatamapItem.id).filter(
            DatamapItem.key == cell.cell_key).all()[0][0]

        return_item = ReturnItem(
            project_id=project_id,
            quarter_id=quarter_id,
            datamap_item_id=cell_val_id,
            value=cell.cell_value)
        session.add(return_item)
    session.commit()


def import_all_returns_to_database():
    """
    Runs through a directory of files and calls
    import_single_bicc_return_using_database on each one. Does not distinguish
    between xlsx files and not so ensure no extraenneous files in there.
    """
    returns_dir = os.path.dirname('/home/lemon/Documents/bcompiler/source/'
                                  'returns/')
    for f in os.listdir(returns_dir):
        print("Importing {}".format(f))
        import_single_bicc_return_using_database(os.path.join(returns_dir, f))


def main():
#    import_datamap_csv('/home/lemon/Documents/bcompiler/source/'
#                       'datamap-returns-to-master-WITH_HEADER_FORSQLITE')
#    merge_gmpp_datamap('/home/lemon/Documents/bcompiler/source/'
#                       'datamap-master-to-gmpp')
#    populate_projects_table()
#    populate_quarters_table()
    import_all_returns_to_database()


if __name__ == "__main__":
    main()
