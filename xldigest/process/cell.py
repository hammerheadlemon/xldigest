"""
New Cell class for QT redesign - started 18 January 2017.

Do not run this code and expect it to work.
"""


class Cell:
    """
    Purpose of the Cell object is to hold data about a spreadsheet cell.
    They are used to populate a datamap cell_map and to write out data to
    a template.
    """
    def __init__(
            self,
            datamap_id,
            cell_key,
            cell_value,
            cell_reference,
            template_sheet,
            bg_colour,
            fg_colour,
            number_format,
            verification_list):
        self.datamap_id = datamap_id,
        self.cell_key = cell_key
        self.cell_value = None
        self.cell_reference = cell_reference
        self.template_sheet = template_sheet
        self.bg_colour = bg_colour
        self.fg_colour = fg_colour
        self.number_format = number_format
        self.verification_list = verification_list
