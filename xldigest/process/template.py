from typing import List

"""
New FormTemplate class for QT redesign - started 18 January 2017.

Do not run this code and expect it to work.
"""


class FormTemplate:
    """
    FormTemplate is a base class for creating Excel templates, which bcompiler
    writes to and reads from. Should be subclassed.
    """
    def __init__(self, file_name: str, blank: bool) -> None:
        self.file_name = file_name
        self.blank = blank


class BICCTemplate(FormTemplate):
    """
    A template used to collect a BICC return. Represented by an Excel
    workbook.
    """
    def __init__(self, source_file: str, blank: bool=False) -> None:
        """
        Initialising a BICCTemplate object requires an Excel file.
        """
        super(BICCTemplate, self).__init__(source_file, blank)
        self.sheets: List[str] = []
        self.source_file = source_file
        if blank is False:
            self.writeable = True
        else:
            self.writable = False

    def add_sheet(self, sheet_name: str) -> None:
        self.sheets.append(sheet_name)
