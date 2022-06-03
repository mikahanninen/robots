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

        Example.

        .. code-block:: robotframework

            Set Cells  A2:D4  New Value
            # Set value for single cell
            Set Cells  E7  Another One
        """
        range = f"{range}:{range}" if ":" not in range else range
        self.logger.info(f"Set cells {range} with value {value}")
        for row in self.workbook._book.active[range]:
            for cell in row:
                cell.value = f'{value}'

    def set_cells_formula(self, range: str, formula: str = None):
        """Set cell values for range of cells.

        Range is a set using Excel's A1 notation.

        :param range: string defining range for target cells
        :param formula: formula which will be set for each cell

        Example.

        .. code-block:: robotframework

            Set Cells  A2:D4  New Value
            # Set value for single cell
            Set Cells  E7  Another One
        """
        range = f"{range}:{range}" if ":" not in range else range
        for row in self.workbook._book.active[range]:
            for cell in row:
                self.logger.warning(type(cell))
                self.logger.warning(dir(cell))
                cell.value = str(formula)
                self.logger.warning(cell.internal_value)
                self.logger.warning(cell.value)
                self.logger.warning(cell.data_type)

    def set_cells_format(self, range: str, format: str = None):
        """Set cell values for range of cells.

        Range is a set using Excel's A1 notation.

        :param range: string defining range for target cells
        :param formula: formula which will be set for each cell

        Example.

        .. code-block:: robotframework

            Set Cells  A2:D4  New Value
            # Set value for single cell
            Set Cells  E7  Another One
        """
        range = f"{range}:{range}" if ":" not in range else range
        for row in self.workbook._book.active[range]:
            for cell in row:
                cell.value = format

    def clear_cells(
        self, range: str, clearing_method: ClearingMethod = ClearingMethod.NONE
    ):
        """Clear cell values for given range of cells.

        Range is a set using Excel's A1 notation.

        Calls `Set Cells` keyword with predefined values - either `NONE` or `SPACE`.

        :param range: string defining range for target cells
        :param clearing_method: if SPACE then `space` character is entered
         as a cell value. By default, NONE, `None` value is set as a cell value

        Example.

        .. code-block:: robotframework

            Clear Cells  A2:D4  New Value
            # Clear value for single cell and clear with SPACE character

            Clear Cells  E7  SPACE
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

        Example.

        .. code-block:: robotframework

            ${sheet}=  Print Sheet To Console
            ...  header=True
            ...  columns=3
            ...  rows=10
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
