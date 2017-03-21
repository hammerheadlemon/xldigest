from openpyxl import load_workbook

from xldigest.process.cleansers import Cleanser
from xldigest.process.exceptions import (QuarterNotFoundError,
                                         ProjectNotFoundError)
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

    def __init__(self, dm, quarter_id, project_id):
        # TODO function to check that given datamap is "blank"
        self._datamap = dm
        self._data = []
        self.quarter_id = quarter_id
        self.project_id = project_id

    @property
    def data(self):
        return self._data

    @property
    def datamap(self):
        return self._datamap

    def _set_up_session(self):
        """
        Helper method to create a SQLAlchemy session.
        """
        database_file = self._datamap.db_file
        engine_string = "sqlite:///" + database_file
        engine = create_engine(engine_string)
        Session = sessionmaker(bind=engine)
        return Session()

    def _check_params(self):
        """
        Internal method to check that we have valid quarter and project
        ids in the Digest.
        """
        session = self._set_up_session()
        project_ids = session.query(Project.id).all()
        project_ids = [item[0] for item in project_ids]
        quarter_ids = session.query(Quarter.id).all()
        quarter_ids = [item[0] for item in quarter_ids]
        if self.quarter_id not in quarter_ids:
            raise QuarterNotFoundError('Quarter not found in database.')
        elif self.project_id not in project_ids:
            raise ProjectNotFoundError('Quarter not found in database.')

    def read_project_data(self):
        """
        Reads project data from a database, to create a populated cell map
        in Digest.data.
        """
        self._check_params()
        session = self._set_up_session()
        for cell in self._datamap.cell_map:
            # ONLY ACT ON CELLS THAT HAVE A CELL_REFERENCE
            if cell.cell_reference:
                cell.cell_value = session.query(ReturnItem.value).filter(
                    ReturnItem.project_id == self.project_id).filter(
                    ReturnItem.datamap_item_id == DatamapItem.id).filter(
                    ReturnItem.quarter_id == self.quarter_id).filter(
                    DatamapItem.id == cell.datamap_id[0]).first()
                self.data.append(cell)

    def write_to_template(self):
        """
        If self._datamap.template is a blank template, then write_to_template()
        will write the datamap.cell_map to it.
        """
        if self._datamap.template.writable is False:
            self.read_project_data()
            blank = load_workbook(self._datamap.template.file_name)
            for celldata in self.data:
                blank[celldata.template_sheet][
                    celldata.cell_reference].value = celldata.cell_value[0]
            blank.save(self._datamap.template.file_name)

        else:
            raise TemplateError(
                "Cannot write to template which contains source data.")

    def read_template(self):
        """
        Read the relevant values from the template, based on the Datamap.
        Made available in self.data.
        """
        wb = load_workbook(self._datamap.template.source_file)
        for cell in self._datamap.cell_map:
            if cell.cell_reference:
                cell.cell_value = wb[cell.template_sheet][
                    cell.cell_reference].value
                # as long as that value is not None, we cleanse the value
                if cell.cell_value is not None:
                    cleansed = Cleanser(cell.cell_value)
                    cleansed.clean()
                    cell.cell_value = cleansed.string
                self.data.append(cell)
