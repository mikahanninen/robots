*** Settings ***
Library           Collections
Library           RPA.Excel.Files
Library           RPA.Robocorp.WorkItems
Library           RPA.Tables
Library           CustomerLogging

*** Tasks ***
Produce Items
    [Documentation]
    ...    Get source Excel file from work item.
    ...    Read rows from Excel.
    ...    Creates output work items per row.
    ${path}=    Get Work Item File    orders.xlsx    %{ROBOT_ARTIFACTS}${/}orders.xlsx
    Open Workbook    ${path}
    ${table}=    Read Worksheet As Table    header=True
    FOR    ${row}    IN    @{table}
        ${variables}=    Create Dictionary
        ...    Name=${row}[Name]
        ...    Zip=${row}[Zip]
        ...    Item=${row}[Item]
        Create Output Work Item
        ...    variables=${variables}
        ...    save=True
    END
    ${count}=    Get Length    ${table}
    Log    For Robot Framework 1
    Customer Log    Read %{ROBOT_ARTIFACTS}${/}orders.xlsx and created ${count} work items for consumer task
    Log    For Robot Framework 2
