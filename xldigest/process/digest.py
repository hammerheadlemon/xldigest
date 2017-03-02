from openpyxl import load_workbook

from xldigest.process.cleansers import Cleanser
from xldigest.database.models import ReturnItem, DatamapItem, Project

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class TemplateError(Exception):
    pass


class Digest:
    """
    Initialise a Digest object with a Datamap object. Digest.data is a list
    that is empty upon initialisation. To populate it from the
    Datamap.template, call Digest.read_template(). To populate it from the
    Datamap.db_file, call Digest.read_project_data(). The latter can then be
    written to Datamap.template with Digest.write()
    """

    def __init__(self, dm, quarter_id):
        # TODO function to check that given datamap is "blank"
        # It is 'blank' when all Cell.cell_value properties are None.
        # Iiterate through each Cell object in datamap.cell_map:
        #   if every cell_value is not None:
        #       we have a partially populated datamap. Bounce.
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
        engine = create_engine("sqlite:///" + database_file)
        Session = sessionmaker(bind=engine)
        session = Session()
        for cell in self._datamap.cell_map:
            # ONLY ACT ON CELLS THAT HAVE A CELL_REFERENCE
            """
            Objective here is to populate the cell_value field of the Cell
            object for a single project.

            What data do we have at this point?

                Cell(
                    cell_key: string,
                    cell_value: None,
                    cell_reference: string
                )
                project_id
                quarter_id

            So our query is to look at the ReturnItem table
                We need a datamap_id for a field but we don't want to match
                    on the text, so we need to include the datamap_id in the
                    Cell object when that is created. TODO!
                for the value field
                    if project_id AND quarter_id equal what is passed to func
                    if datamap_item_id equals

            """
            if cell.cell_reference:
                cell.cell_value = session.query(ReturnItem.value).filter(
                    ReturnItem.project_id == project_id,
                    ReturnItem.quarter_id == quarter_id,
                    ReturnItem.datamap_item_id == cell.datamap_id)
                # then we append it to self.data
                self.data.append(cell)

    def write(self):
        """
        If self._datamap.template is a blank template, then write() will
        write the datamap.cell_map to it.
        """
        if self.dm.template.writable is False:
            pass  # do stuff to write
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
