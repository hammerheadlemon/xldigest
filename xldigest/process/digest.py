import fnmatch
import os
from concurrent import futures
from datetime import datetime

from openpyxl import load_workbook

from xldigest.process.cleansers import Cleanser


class Digest:
    """
    A Digest is a Datamap object whose cell_map has been populated (ie
    the datamap 'cell_value' has been populated by data in a particular
    template source file.
    """

    def __init__(self, dm):
        # TODO function to check that given datamap is "blank"
        # It is 'blank' when all Cell.cell_value properties are None.
        # Iiterate through each Cell object in datamap.cell_map:
        #   if every cell_value is not None:
        #       we have a partially populated datamap. Bounce.
        self._datamap = dm
        self._data = []

    @property
    def data(self):
        return self._data

    @property
    def datamap(self):
        return self._datamap

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


def flatten_project(future):
    """
    Get rid of the gmpp_key gmpp_key_value stuff pulled from a single
    spreadsheet. Must be given a future.
    """
    p_data = future.result()
    p_data = {item['gmpp_key']: item['gmpp_key_value'] for item in p_data}
    return p_data


def digest_source_files(base_dir, db_connection):
    """
    Use concurrent futures to digest data obtained using legacy
    parse_source_cells function.
    """
    source_files = []
    future_data = []
    for f in os.listdir(base_dir):
        if fnmatch.fnmatch(f, '*.xlsx'):
            source_files.append(os.path.join(base_dir, f))
    with futures.ThreadPoolExecutor(max_workers=4) as executor:
        for f in source_files:
            future_data.append(
                executor.submit(parse_source_cells, f,
                                DATAMAP_MASTER_TO_RETURN))
            print("Processing {}".format(f))
        for future in futures.as_completed(future_data):
            f = flatten_project(future)
            db.insert(f)


def main():
    digest_source_files()


if __name__ == "__main__":
    main()
