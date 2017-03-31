import os
import appdirs

from xldigest.process.exceptions import NoFilesInDirectoryError

from openpyxl import load_workbook

APPNAME = 'xldigest'
APPAUTHOR = 'MRLemon'
USER_DATA_DIR = appdirs.user_data_dir(APPNAME, APPAUTHOR)


class Ingestor:
    def __init__(self,
                 source_dir: str,
                 portfolio: int,
                 series: int,
                 series_item: int) -> None:
        self.source_dir = source_dir
        self.portfolio = portfolio
        self.series = series
        self.series_item = series_item

    def _set_up_cache(self) -> None:
        pass

    def source_xls_only(self) -> bool:
        fls = os.listdir(self.source_dir)
        if len(fls) > 0:
            for f in fls:
                try:
                    load_workbook(self.source_dir + '/' + f)
                except:
                    print(f"{f} - that's not an xlsx file")
                    return False
            return True
        else:
            raise NoFilesInDirectoryError

    def __repr__(self):
        return "Ingestor()"

    def __str__(self):
        return "Ingestor()"
