*** Settings ***
Library     ExtendedExcelLibrary.py
Library     RPA.Tables
Library     OperatingSystem


*** Tasks ***
Creating new excel
    Open Workbook    ${CURDIR}${/}backup.xlsx
    Log To Console    \nExcel operations
    ${sheet}=    Print Sheet To Console
    ...    header=True
    ...    columns=5
    ...    rows=5
    Clear Cells    A2:B5
    Set Cells    D2    Completed
    Set Cells    F3    =COUNTIF(D:D,"=Completed")
    Set Cells Formula    G2    G3:G99    =C2+5
    Print Sheet To Console
    ...    header=True
    ...    columns=7
    ...    rows=5
    Save Workbook    ${CURDIR}${/}temp.xlsx
    Close Workbook
    Log    Done.

Working with one excel
    Copy File    ${CURDIR}${/}backup.xlsx    ${CURDIR}${/}work.xlsx
    Open Workbook    ${CURDIR}${/}work.xlsx
    Log To Console    \nExcel operations
    ${sheet}=    Print Sheet To Console
    ...    header=True
    ...    columns=5
    ...    rows=6
    # Clearing and setting cell value and formulas
    Clear Cells    A2:B5
    Set Cells    C4    15
    Set Cells    D2    Completed
    Set Cells    F4    total_completed
    Set Cells    F5    =COUNTIF(D:D,"=Completed")
    Set Cells    F6    total_not_started
    Set Cells    F7    =COUNTIF(D:D,"=NotStarted")
    #    Append rows to existing Workbook
    FOR    ${value}    IN RANGE    10
        ${newvalue}=    Evaluate    300+$value+($value*2)
        &{row}=    Create Dictionary
        ...    name=hello world
        ...    type=new
        ...    id=${newvalue}
        ...    status=NotStarted
        Append rows to worksheet    ${row}    header=True
    END

    # Set formula to cell G2 and translate that formula for cells G3:G30
    Set Cells Formula    G2    G3:G30    =C2+5
    Print Sheet To Console
    ...    header=True
    ...    columns=7
    ...    rows=6
    Align Cells    C1:C100
    Align Cells    F1:F100
    Save Workbook
    Close Workbook
    Log    Done.
