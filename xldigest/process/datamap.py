import csv
import sqlite3

from xldigest.process.cell import Cell

"""
New Datamap class for QT redesign - started 18 January 2017.

Do not run this code and expect it to work.
"""


class Datamap:
    """
    Purpose of the Datamap is to map key/value sets to the database and a
    FormTemplate class. A Datamap comprises a list of Cell objects.
    """
    def __init__(self, template, db_file):
        self.cell_map = []
        self.template = template
        self.db_file = db_file

    def add_cell(self, cell):
        self.cell_map.append(cell)
        return cell

    def delete_cell(self, cell):
        self.cell_map.remove(cell)
        return cell

    def import_csv(self, source_file):
        """
        Read from a CSV source file. Returns a list of corresponding Cell
        objects.
        """
        if source_file[-4:] == '.csv':
            try:
                self._import_source_data(source_file)
            except Exception:
                print("Problem with that CSV file. File extension?")

    def _import_source_data(self, source_file):
        """Internal implementation of csv importer."""
        with open(source_file, 'r') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                self.cell_map.append(
                        Cell(
                            cell_key=row['cell_key'],
                            cell_value=None,  # have no need of a value in dm
                            cell_reference=row['cell_reference'],
                            template_sheet=row['template_sheet'],
                            bg_colour=row['bg_colour'],
                            fg_colour=row['fg_colour'],
                            number_format=row['number_format'],
                            verification_list=None
                            )
                        )

    def cell_map_from_database(self):
        """Creates a cellmap from a sqlite3 database."""
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()
        for row in c.execute("SELECT * FROM datamap_items"):
            self.cell_map.append(
                Cell(
                    cell_key=row[1],
                    cell_value=None,
                    template_sheet=row[2],
                    bg_colour=None,
                    fg_colour=None,
                    number_format=None,
                    verification_list=None,
                    cell_reference=row[3]))
        c.close()
        conn.close()
