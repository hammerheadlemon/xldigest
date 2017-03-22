from openpyxl import load_workbook

from typing import Tuple, Any, List

from xldigest.process.cleansers import Cleanser
from xldigest.process.datamap import Datamap
from xldigest.process.cell import Cell
from xldigest.process.exceptions import (QuarterNotFoundError,
                                         ProjectNotFoundError,
                                         DuplicateReturnError)
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

    def __init__(self, dm: Datamap, quarter_id: int, project_id: int) -> None:
        self._datamap = dm
        self._data: List[Cell] = []
        self._existing_quarter_ids = \
            self._get_existing_project_and_quarter_ids()[0]
        self._existing_project_ids = \
            self._get_existing_project_and_quarter_ids()[1]
        self._get_existing_return_project_and_quarter_ids()

        self.quarter_id = quarter_id
        self.project_id = project_id

    @property
    def data(self) -> List[Cell]:
        return self._data

    @property
    def datamap(self) -> Datamap:
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

    def _get_existing_project_and_quarter_ids(self) -> Tuple[Any, Any]:
        """
        Returns a tuple of lists of quarter_ids and project_ids
        in the database.
        """
        session = self._set_up_session()
        project_ids = session.query(Project.id).all()
        quarter_ids = session.query(Quarter.id).all()
        session.close()
        return quarter_ids, project_ids

    def _get_existing_return_project_and_quarter_ids(self) -> None:
        """
        Generate a set containing project_ids in returns, and a set containing
        quarter_ids in returns.
        """
        session = self._set_up_session()
        project_ids_in_returns = session.query(ReturnItem.project_id).all()
        quarter_ids_in_returns = session.query(ReturnItem.quarter_id).all()
        self._existing_project_ids_in_returns = {
            id[0] for id in project_ids_in_returns}
        self._existing_quarter_ids_in_returns = {
            id[0] for id in quarter_ids_in_returns}
        session.close()

    def _check_quarter_exists_in_db(self) -> None:
        """
        Raise QuarterNotFoundError if there is no corresponding quarter_id in
        Digest object.
        """
        session = self._set_up_session()
        quarter_ids = session.query(Quarter.id).all()
        quarter_ids = [item[0] for item in quarter_ids]
        if self.quarter_id not in quarter_ids:
            session.close()
            raise QuarterNotFoundError('Quarter not found in database.')
        session.close()

    def _check_project_exists_in_db(self) -> None:
        """
        Raise ProjectNotFoundError if there is no corresponding project_id in
        Digest object.
        """
        session = self._set_up_session()
        project_ids = session.query(Project.id).all()
        project_ids = [item[0] for item in project_ids]
        if self.project_id not in project_ids:
            session.close()
            raise ProjectNotFoundError('Project not found in database.')
        session.close()

    def read_project_data(self) -> None:
        """
        Reads project data from a database, to create a populated cell map
        in Digest.data.
        """
        self._check_quarter_exists_in_db()
        self._check_project_exists_in_db()
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
        session.close()

    def write_to_template(self) -> None:
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

    def _check_for_existing_return(self) -> bool:
        """
        Checks for existence of any returns in database matching qtr_id and
        pjt_id. If there are already records in there with these values,
        we're going to be duplicating returns, therefore this is not allowed.
        """
        if self.project_id in self._existing_project_ids_in_returns \
                and self.quarter_id in self._existing_quarter_ids_in_returns:
            return False
        else:
            return True

    def write_to_database(self) -> None:
        """
        Checks whether there is a quarter and a project in the database that
        corresponds with the Digest data we wish to import into the database.
        If there isn't, an appropriate exception is raised.

        If we go ahead, we then check whether there is already a return in the
        database with the same quarter/project_id combination. If there is,
        we should not be importing this Digest and an appropriate exception
        is raised.

        Otherwise, write the Digest data to the database.
        """
        self._check_quarter_exists_in_db()
        self._check_project_exists_in_db()
        if self._check_for_existing_return():
            session = self._set_up_session()
            for cell in self._data:
                return_item = ReturnItem(
                    project_id=self.project_id,
                    quarter_id=self.quarter_id,
                    datamap_item_id=cell.datamap_id[0],
                    value=cell.cell_value)
                session.add(return_item)
            session.commit()
            session.close()
        else:
            raise DuplicateReturnError(
                "Existing records in database with quarter_id:"
                " {} project_id: {}".format(self.quarter_id, self.project_id))

    def read_template(self) -> None:
        """
        Read the relevant values from the template, based on the Datamap.
        Made available in self.data.
        """
        wb = load_workbook(self._datamap.template.file_name)
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
