import csv
import sqlite3

from xldigest.process.cell import Cell

from xldigest.database.models import DatamapItem

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:////home/lemon/code/python/xldigest/xldigest/'
                       'db.sqlite')
Session = sessionmaker(bind=engine)
session = Session()


class Datamap:
    """
    Purpose of the Datamap is to map key/value sets to the database and a
    FormTemplate class. A Datamap comprises a list of Cell objects.

    Newly initialised Datamap object contains a template and a reference to
    a SQLite database file, but it's cell_map is empty. To create a base cell
    map from the template, using the datamap table in the database, call
    Datamap.cell_map_from_database(). To create a base cell map from the
    template, call Datamap.import_csv().
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
                            datamap_id=None,
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
        """Creates a cellmap from a sqlite3 database. cell_map fields are
        empty until a function is called to populate the cellmap from
        a data source."""
        for row in session.query(DatamapItem).all():
            self.cell_map.append(
                Cell(
                    datamap_id=row.id,  # for now...
                    cell_key=row.key,
                    cell_value=None,
                    template_sheet=row.bicc_sheet,
                    bg_colour=None,
                    fg_colour=None,
                    number_format=None,
                    verification_list=None,
                    cell_reference=row.bicc_cellref))
