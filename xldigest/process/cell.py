"""
New Cell class for QT redesign - started 18 January 2017.

Do not run this code and expect it to work.
"""

from typing import Any, Union


class Cell:
    """
    Purpose of the Cell object is to hold data about a spreadsheet cell.
    They are used to populate a datamap cell_map and to write out data to
    a template.
    """
    def __init__(self,
                 datamap_id: Union[int, None],
                 cell_key: str,
                 cell_value: Any,
                 cell_reference: str,
                 template_sheet: str,
                 bg_colour: Union[str, None],
                 fg_colour: Union[str, None],
                 number_format: Union[str, None],
                 verification_list: Union[str, None]) -> None:
        self.datamap_id = datamap_id,
        self.cell_key = cell_key
        self.cell_value = None  # type: Any
        self.cell_reference = cell_reference
        self.template_sheet = template_sheet
        self.bg_colour = bg_colour
        self.fg_colour = fg_colour
        self.number_format = number_format
        self.verification_list = verification_list

    def __repr__(self) -> str:
        return ("<Cell: DMID:{} CellKey:{} CellValue:{} CellRef:{} "
                "Sheet:{}>".format(
                    self.datamap_id,
                    self.cell_key,
                    self.cell_value,
                    self.cell_reference,
                    self.template_sheet))
