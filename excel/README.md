# Extended RPA.Excel.Files Robot

This Robot demonstrates extending [rpaframework](https://github.com/robocorp/rpaframework) [RPA.Excel.Files](https://robocorp.com/docs/libraries/rpa-framework/rpa-excel-files) library.

There experimental keywords like `Set Cells`, `Clear Cells` and `Print Sheet To Console` have been added to the list of default available [keywords](https://robocorp.com/docs/libraries/rpa-framework/rpa-excel-files/keywords).

```robot
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
```

## Keyword `Set Cells`

Can be used to set value for a cell or range of cells using Excel's A1 notation.

## Keyword `Clear Cells`

Can be used to clear value for a cell or range of cells using Excel's A1 notation. By default keyword will set value of the cells to None, but
value can be set to EMPTY (space character).

## Keyword `Print Sheet To Console`

Uses keyword `Read Worksheet` to read Excel worksheet into memory and then prints its contents into the console and at the end returns the sheet.

Example output from task execution. Shows table content before modifications and after.

Original sheet cells A2:B5 are cleared and cell D2 value is set to 'Completed'.

<img src="images/example_console_output.png" style="margin-bottom:20px; width: 600px;">

## Learning materials

- [All docs related to Robot Framework](https://robocorp.com/docs/languages-and-frameworks/robot-framework)
