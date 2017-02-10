import csv
import os
import sqlite3
import sys

from bcompiler.datamap import Datamap
from bcompiler.process.digest import Digest
from bcompiler.template import BICCTemplate


# Hard-coded for now - this matches the current quarter with the same
# value in the database so we're not relying on how it's written in
# BICC template.
CURRENT_QUARTER = "Q3 2016/17"


def create_tables():
    """Drop table before creation"""

    conn = sqlite3.connect('db.sqlite')
    c = conn.cursor()

    c.execute('DROP TABLE IF EXISTS project')
    c.execute("""\
              CREATE TABLE project
              (
              project_id INTEGER PRIMARY KEY,
              name TEXT
              )
              """)

    c.execute('DROP TABLE IF EXISTS quarter')
    c.execute("""\
              CREATE TABLE quarter
              (
              quarter_id INTEGER PRIMARY KEY,
              name TEXT
              )
              """)

    c.execute('DROP TABLE IF EXISTS datamap_item')
    c.execute("""\
              CREATE TABLE datamap_item
              (
              datamap_item_id INTEGER PRIMARY KEY,
              key TEXT,
              bicc_sheet TEXT,
              bicc_cellref TEXT,
              gmpp_sheet TEXT,
              gmpp_cellref TEXT,
              bicc_verification_formula TEXT
              )
              """)

    c.execute('DROP TABLE IF EXISTS returns')
    c.execute("""\
              CREATE TABLE returns
              (
              returns_id INTEGER PRIMARY KEY,
              value TEXT,
              project_id INTEGER REFERENCES project (project_id),
              quarter_id INTEGER REFERENCES quarter (quarter_id),
              datamap_id INTEGER REFERENCES datamap_item (datamap_id),
              timestamp TEXT
              )
              """)
    conn.commit()
    c.close()
    conn.close()


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
    conn = sqlite3.connect('db.sqlite')
    c = conn.cursor()

    with open(source_file, 'r') as f:
        reader = csv.DictReader(f)
        #       # DON'T NEED TIMESTAMP STUFF HERE BUT LEAVING IF FOR
        #       # IMPORT FROM RETURN FUNCTION WHEN CREATED
        #       time_stamp = time.time()
        #       date = str(
        #           datetime.datetime.fromtimestamp(time_stamp).strftime(
        #               '%d-%m-%Y %H:%M:%S'))
        for row in reader:
            row = _change_dict_val("", None, row)
            row = _strip_trailing_whitespace(row)
            c.execute("""\
                      INSERT INTO datamap_item (
                      key,
                      bicc_sheet,
                      bicc_cellref,
                      bicc_verification_formula
                      ) VALUES (?, ?, ?, ?)
                      """, (row['key'], row['bicc_sheet'], row['bicc_cellref'],
                            row['bicc_verification_formula']))
        conn.commit()
        c.close()
        conn.close()


def merge_gmpp_datamap(source_file):
    """
    Merge-in relevant cell references from a GMPP-based datamap, based on
    values from the returns-to-master datamap.
    """
    conn = sqlite3.connect('db.sqlite')
    c = conn.cursor()

    keys = [result[0] for result in c.execute("SELECT key FROM datamap_item")]

    with open(source_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            row = _change_dict_val("", None, row)
            row = _strip_trailing_whitespace(row)
            if row['master_cellname'] in keys:
                c.execute("""\
                          UPDATE datamap_item
                          SET gmpp_cellref=(?), gmpp_sheet=(?)
                          WHERE key=(?)""",
                          (row['gmpp_template_cell_reference'],
                           row['gmpp_template_sheet_reference'],
                           row['master_cellname']))
    conn.commit()
    c.close()
    conn.close()


def populate_quarters_table():
    """
    Populate basic Quarter information.
    """
    conn = sqlite3.connect('db.sqlite')
    c = conn.cursor()
    c.execute("INSERT INTO quarter (name) VALUES (?)", ("Q2 2016/17",))
    c.execute("INSERT INTO quarter (name) VALUES (?)", ("Q3 2016/17",))
    c.execute("INSERT INTO quarter (name) VALUES (?)", ("Q4 2016/17",))
    c.execute("INSERT INTO quarter (name) VALUES (?)", ("Q1 2017/18",))
    c.execute("INSERT INTO quarter (name) VALUES (?)", ("Q2 2017/18",))
    c.execute("INSERT INTO quarter (name) VALUES (?)", ("Q3 2017/18",))
    c.execute("INSERT INTO quarter (name) VALUES (?)", ("Q4 2017/18",))
    c.execute("INSERT INTO quarter (name) VALUES (?)", ("Q1 2018/19",))
    c.execute("INSERT INTO quarter (name) VALUES (?)", ("Q2 2018/19",))
    conn.commit()
    c.close()
    conn.close()


def populate_projects_table():
    """
    Populate the project table in the database. The master_transposed.csv
    file is used as the source for this.
    """
    conn = sqlite3.connect('db.sqlite')
    c = conn.cursor()
    with open('/home/lemon/Documents/bcompiler/source/master_transposed.csv'
              ) as f:
        reader = csv.DictReader(f)
        project_list = [row['Project/Programme Name'] for row in reader]
        for p in project_list:
            c.execute("INSERT INTO project (name) VALUES (?)", (p, ))
    conn.commit()
    c.close()
    conn.close()


def import_single_bicc_return_using_database(source_file):
    """
    Import a single BICC return based on a source template. Use the datamap
    from database, rather than the csv file.
    """
    conn = sqlite3.connect('db.sqlite')
    c = conn.cursor()
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
    project_id = c.execute(
        "SELECT project_id FROM project WHERE project.name=(?)",
        (project_name[0],))
    try:
        project_id = tuple(project_id)[0][0]
    except IndexError:
        print("{} may not be in project table in database. Check it."
              " Will not import this time".format(project_name[0]))
        project_id = None

    # we need quarter_id to build the tables
    quarter_id = c.execute(
        "SELECT quarter_id FROM quarter WHERE "
        "quarter.name=(?)", (CURRENT_QUARTER,))
    quarter_id = tuple(quarter_id)[0][0]

    # go through the cell_map in the Digest object and drop into database
    for cell in digest.data:
        cell_val_id = c.execute(
            "SELECT datamap_item_id from datamap_item WHERE "
            "datamap_item.key=?",
            (cell.cell_key,))
        cell_val_id = tuple(cell_val_id)[0][0]
        c.execute("""\
                  INSERT INTO returns (
                  datamap_id,
                  value,
                  project_id,
                  quarter_id
                  ) VALUES (?, ?, ?, ?)
                  """, (cell_val_id, cell.cell_value, project_id, quarter_id))
    conn.commit()
    c.close()
    conn.close()


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
    """
    This is here to allow us to call the importation stuff from the
    command line.
    """
    try:
        if sys.argv[1]:
            create_tables()
            import_datamap_csv(
                '/home/lemon/Documents/bcompiler/source/'
                'datamap-returns-to-master-WITH_HEADER_FORSQLITE')
            merge_gmpp_datamap('/home/lemon/Documents/bcompiler/source'
                               '/datamap-master-to-gmpp')
            populate_projects_table()
            populate_quarters_table()
    except:
        import_all_returns_to_database()


if __name__ == "__main__":
    main()