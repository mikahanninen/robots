from RPA.Excel.Files import Files

class CustomExcel(Files):

    def __init__(self):
        super().__init__()

    def copypaste(self, rows, columns):
        data = []
        #for col in self.active.iter_cols(min_row=4, min_col=1, max_row=10, max_col=4):
        # COPY
        for row in range(4, 11):
            for column in range(1,5):
                cell = self.workbook.book.active.cell(row, column)
                data.append(cell)
                self.logger.warning(dir(cell))
                break
            break
        # PASTE
        # value, style, number_format, hyperlink, alignment, border, comment, data_type, protection?, pivotButton?
        
        #for row in range(1, 8):
        #    for column in range(1,5):
        #        index = (row-1)*(column-1)
        #        self.workbook.book.active.cell(row, column) = data[index]
        #        data.append(cell)        
        return data
