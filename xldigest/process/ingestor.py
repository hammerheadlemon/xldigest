import os

from openpyxl import load_workbook


class NoFilesInDirectoryError(Exception):
    pass


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

    def source_xls_only(self):
        fls = os.listdir(self.source_dir)
        if len(fls) > 0:
            for f in fls:
                try:
                    load_workbook(self.source_dir + '/' + f)
                except:
                    print("No")
                    return False
                else:
                    return True
        else:
            raise NoFilesInDirectoryError

    def __repr__(self):
        return "Ingestor()"

    def __str__(self):
        return "Ingestor()"
