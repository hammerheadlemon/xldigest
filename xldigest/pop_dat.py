import csv
# import datetime
import sqlite3
# import time

conn = sqlite3.connect('db.sqlite')
c = conn.cursor()


def create_tables():
    """Drop table before creation"""

    c.execute('DROP TABLE IF EXISTS project')
    c.execute("""\
              CREATE TABLE project
              (
              id INTEGER PRIMARY KEY,
              name TEXT
              )
              """)

    c.execute('DROP TABLE IF EXISTS quarter')
    c.execute("""\
              CREATE TABLE quarter
              (
              id INTEGER PRIMARY KEY,
              name TEXT
              )
              """)

    c.execute('DROP TABLE IF EXISTS datamap')
    c.execute("""\
              CREATE TABLE datamap
              (
              id INTEGER PRIMARY KEY,
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
              id INTEGER PRIMARY KEY,
              key TEXT,
              value TEXT,
              project INTEGER REFERENCES project (id),
              quarter INTEGER REFERENCES quarter (id),
              timestamp TEXT
              )
              """)
    conn.commit()
    c.close()
    conn.close()


def import_csv(source_file):

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
            c.execute("""\
                      INSERT INTO datamap (
                      key,
                      bicc_sheet,
                      bicc_cellref,
                      bicc_verification_formula
                      ) VALUES (?, ?, ?, ?)
                      """,
                      (row['key'],
                       row['bicc_sheet'],
                       row['bicc_cellref'],
                       row['bicc_verification_formula']))
        conn.commit()
        c.close()
        conn.close()


def merge_gmpp_datamap(source_file):
    # first we get a lost of all keys from db
    conn = sqlite3.connect('db.sqlite')
    c = conn.cursor()

    keys = [result[0] for result in c.execute("SELECT key FROM datamap")]

    with open(source_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['master_cellname'] in keys:
                c.execute("""\
                          UPDATE datamap
                          SET gmpp_cellref=(?), gmpp_sheet=(?)
                          WHERE key=(?)""", (
                              row['gmpp_template_cell_reference'],
                              row['gmpp_template_sheet_reference'],
                              row['master_cellname']
                          ))
    conn.commit()
    c.close()
    conn.close()


create_tables()
import_csv('/home/lemon/Documents/bcompiler/source/datamap-returns-'
           'to-master-WITH_HEADER_FORSQLITE')
merge_gmpp_datamap('/home/lemon/Documents/bcompiler/source'
                   '/datamap-master-to-gmpp')
