*** Settings ***
Library     ExtendedExcelLibrary.py


*** Tasks ***
Minimal task
    [Setup]    Open Workbook    ${CURDIR}${/}work.xlsx
    Log To Console    \nExcel operations
    ${sheet}=    Print Sheet To Console    header=True    columns=5    rows=5
    Clear Cells    A2:B5
    Set Cells    D2    Completed
    Print Sheet To Console    header=True    columns=5    rows=5
    Save Workbook    ${CURDIR}${/}temp.xlsx
    Log    Done.
    [Teardown]    Close Workbook
