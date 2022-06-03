*** Settings ***
Library     ExtendedExcelLibrary.py


*** Tasks ***
Minimal task
    Open Workbook    ${CURDIR}${/}work.xlsx
    Log To Console    \nExcel operations
    ${sheet}=    Print Sheet To Console
    ...    header=True
    ...    columns=5
    ...    rows=5
    Clear Cells    A2:B5
    Set Cells    D2    Completed
    Set Cells Formula    F3    =COUNTIF(D:D,"=Completed")
    Print Sheet To Console
    ...    header=True
    ...    columns=6
    ...    rows=5
    Save Workbook    ${CURDIR}${/}temp.xlsx
    Close Workbook
    Open Workbook    ${CURDIR}${/}temp.xlsx    data_only=True
    ${sheet}=    Print Sheet To Console
    ...    header=True
    ...    columns=6
    ...    rows=5
    Close Workbook
    Open Workbook    ${CURDIR}${/}work.xlsx    data_only=True
    ${sheet}=    Print Sheet To Console
    ...    header=True
    ...    columns=6
    ...    rows=5
    Close Workbook
    Log    Done.
