import csv
import sqlite3

from bcompiler.datamap import Datamap
from bcompiler.process.digest import Digest
from bcompiler.template import BICCTemplate

conn = sqlite3.connect('db.sqlite')
c = conn.cursor()

CURRENT_QUARTER = "Q3 2016/17"


def create_tables():
    """Drop table before creation"""

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


def change_dict_val(target, replacement, dictionary):
    for k, v in dictionary.items():
        if v == target:
            dictionary[k] = replacement
    return dictionary


def strip_trailing_whitespace(dictionary):
    for k, v in dictionary.items():
        # probably a string
        if isinstance(v, str):
            dictionary[k] = v.rstrip()
    return dictionary


def import_datamap_csv(source_file):

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
            row = change_dict_val("", None, row)
            row = strip_trailing_whitespace(row)
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
    # first we get a lost of all keys from db
    conn = sqlite3.connect('db.sqlite')
    c = conn.cursor()

    keys = [result[0] for result in c.execute("SELECT key FROM datamap_item")]

    with open(source_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            row = change_dict_val("", None, row)
            row = strip_trailing_whitespace(row)
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
    conn = sqlite3.connect('db.sqlite')
    c = conn.cursor()
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


def import_single_bicc_return_using_database():
    conn = sqlite3.connect('db.sqlite')
    c = conn.cursor()
    BICC = ('/home/lemon/Documents/bcompiler/source/returns/'
            'Crossrail _Q3_Return_Final.xlsx')
    template = BICCTemplate(BICC)
    datamap = Datamap(template,
                      '/home/lemon/code/python/xldigest/xldigest/db.sqlite')
    datamap.cell_map_from_database()
    digest = Digest(datamap)
    digest.read_template()
    project_name = [
        item.cell_value for item in datamap.cell_map
        if item.cell_key == 'Project/Programme Name'
    ]

    project_id = c.execute(
        "SELECT project_id FROM project WHERE project.name=(?)", project_name)
    project_id = tuple(project_id)[0][0]
    quarter_id = c.execute(
        "SELECT quarter_id FROM quarter WHERE "
        "quarter.name=(?)", (CURRENT_QUARTER,))
    quarter_id = tuple(quarter_id)[0][0]
    print("\n")
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


# create_tables()
# import_datamap_csv('/home/lemon/Documents/bcompiler/source/datamap-returns-'
#                    'to-master-WITH_HEADER_FORSQLITE')
# merge_gmpp_datamap('/home/lemon/Documents/bcompiler/source'
#                    '/datamap-master-to-gmpp')
#populate_projects_table()
#populate_quarters_table()
import_single_bicc_return_using_database()
