from openpyxl import load_workbook

from xldigest.process.cleansers import Cleanser
from xldigest.database.models import ReturnItem, DatamapItem, Project, Quarter

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class TemplateError(Exception):
    pass


class Digest:
    """
    Initialise a Digest object with a Datamap object. Digest.data is a list
    that is empty upon initialisation.

    To populate it from the Datamap.template, call Digest.read_template().
    To populate it from the Datamap.db_file, call Digest.read_project_data().
    The latter can then be written to Datamap.template with Digest.write()

    To create a Digest object for writing to a template:
        - create a template object with the template you wish to populate.
        e.g bicc_template = BICCTemplate(<path-to-file>)

        - create an 'empty' datamap, based on this template:
        e.g base_datamap = Datamap(bicc_template, <path-to-db-file>)

        - create a Digest object:
        e.g. digest = Digest(base_datamap, <quarter-id>)

        - populate the datamap from the database:
        e.g. digest.data.cell_map_from_database()

        - populate the digest.data with either data from the template
        (if the template is non-writable) or from the database. The Digest
        then acts as the intermediadary between the template and database.

        Data from database:
            digest.read_project_data(<quarter-id>, <project-id>)
            digest.data

        Data from template:
            digest.read_template()
            digest.data
    """

    def __init__(self, dm, quarter_id):
        # TODO function to check that given datamap is "blank"
        self._datamap = dm
        self._data = []
        self.quarter_id = quarter_id

    @property
    def data(self):
        return self._data

    @property
    def datamap(self):
        return self._datamap

    def read_project_data(self, project_id, quarter_id):
        database_file = self._datamap.db_file
        engine_string = "sqlite:///" + database_file
        engine = create_engine(engine_string)
        Session = sessionmaker(bind=engine)
        session = Session()
        for cell in self._datamap.cell_map:
            # ONLY ACT ON CELLS THAT HAVE A CELL_REFERENCE
            if cell.cell_reference:
                cell.cell_value = session.query(ReturnItem.value).filter(
                    ReturnItem.project_id == Project.id).filter(
                    ReturnItem.datamap_item_id == DatamapItem.id).filter(
                    DatamapItem.key == cell.cell_key).first()
                # then we append it to self.data
                self.data.append(cell)

    def write(self):
        """
        If self._datamap.template is a blank template, then write() will
        write the datamap.cell_map to it.
        """
        if self.dm.template.writable is False:
            pass  # do stuff to write - consider compile.py in bcompiler
        else:
            raise TemplateError(
                "Cannot write to template which contains source data.")

    def read_template(self):
        """
        Read the relevant values from the template, based on the Datamap.
        Made available in self.data.
        """
        # load the template
        wb = load_workbook(self._datamap.template.source_file)
        # go through each Cell in datamap.cell_map
        for cell in self._datamap.cell_map:
            # ONLY ACT ON CELLS THAT HAVE A CELL_REFERENCE
            if cell.cell_reference:
                # get value of cell from the template file
                cell.cell_value = wb[cell.template_sheet][
                    cell.cell_reference].value
                # as long as that value is not None, we cleanse the value
                if cell.cell_value is not None:
                    cleansed = Cleanser(cell.cell_value)
                    cleansed.clean()
                    cell.cell_value = cleansed.string
                # then we append it to self.data
                self.data.append(cell)
