from prettytable import PrettyTable
from robot.libraries.BuiltIn import BuiltIn

from RPA.Excel.Files import Files
from RPA.Tables import Tables
from enum import Enum


class ClearingMethod(Enum):

    SPACE = " "
    NONE = None


class ExtendedExcelLibrary(Files):
    def __init__(self, *args, **kwargs) -> None:
        Files.__init__(self, *args, **kwargs)

    def set_cells(self, range: str, value: str = None):
        """Set cell values for range of cells.

        Range is a set using Excel's A1 notation.

        :param range: string defining range for target cells
        :param value: value which will be set for each cell
        """
        range = f"{range}:{range}" if ":" not in range else range
        for row in self.workbook._book.active[range]:
            for cell in row:
                cell.value = value

    def clear_cells(
        self, range: str, clearing_method: ClearingMethod = ClearingMethod.NONE
    ):
        """Clear cell values for given range of cells.

        Range is a set using Excel's A1 notation.

        Calls `Set Cells` keyword with predefined values - either `NONE` or `SPACE`.

        :param range: string defining range for target cells
        :param clearing_method: if SPACE then `space` character is entered
         as a cell value. By default, NONE, `None` value is set as a cell value
        """
        self.set_cells(range, clearing_method.value)

    def print_sheet_to_console(
        self, header: bool = False, columns: int = None, rows: int = None
    ):
        """Print worksheet read by `Read Worksheet` keyword into console
        and return worksheet.

        :param header: does data have headers, will affect print and
         returned `sheet`
        :param columns: maximum columns to print
        :param rows: maximum rows to print
        :return: sheet as read by `Read Worksheet` keyword
        """
        sheet = self.read_worksheet(header=header)
        rpa_table = Tables().create_table(sheet)
        pt = PrettyTable()
        pt.field_names = rpa_table.columns[:columns] if columns else rpa_table.columns
        for index, row in enumerate(rpa_table):
            if rows and (index + 1) > rows:
                break
            values = list(row.values())
            values = values[:columns] if columns else values
            pt.add_row(values)
        BuiltIn().log_to_console(f"\n{pt}")
        return sheet
