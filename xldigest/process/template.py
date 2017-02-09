"""
New FormTemplate class for QT redesign - started 18 January 2017.

Do not run this code and expect it to work.
"""


class FormTemplate:
    """
    FormTemplate is a base class for creating Excel templates, which bcompiler
    writes to and reads from. Should be subclassed.
    """
    def __init__(self, file_name):
        self.file_name = file_name


class BICCTemplate(FormTemplate):
    """
    A template used to collect a BICC return. Represented by an Excel
    workbook.
    """
    def __init__(self, source_file):
        """
        Initialising a BICCTemplate object requires an Excel file.
        """
        super(BICCTemplate, self).__init__(source_file)
        self.sheets = []
        self.source_file = source_file

    def add_sheet(self, sheet_name):
        self.sheets.append(sheet_name)
