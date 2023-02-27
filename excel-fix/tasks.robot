*** Settings ***
Library     CustomExcel
Library     OperatingSystem
Library     Collections


*** Tasks ***
Minimal task
    Copy File
    ...    E:\\koodi\\testground\\excel-fix-delete-rows\\test.xlsx
    ...    E:\\koodi\\testground\\excel-fix-delete-rows\\work.xlsx
    Open Workbook    E:\\koodi\\testground\\excel-fix-delete-rows\\work.xlsx
    #Move Range    A4:D10    -3
    ${data}=    Copypaste    4    4
    Log List    ${data}    level=WARN
    Save Workbook
    Log    Done.
