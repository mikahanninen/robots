*** Settings ***
Library     RPA.Browser.Selenium
Library     Collections
Library     RPA.Tables


*** Variables ***
${WEBSITE}                      https://mdbootstrap.com/docs/b4/jquery/tables/pagination/
${LOCATOR_TABLE_HEADINGS}       //table[@id='dtBasicExample']//thead//th
${LOCATOR_TABLE_ROWS}           //table[@id='dtBasicExample']//tbody//tr
${LOCATOR_NEXT_BUTTON}          //a[text()="Next"]/parent::li


*** Test Cases ***
Minimal task
    # Action: Scrape all table pages and return headers + rows
    ${headers}    ${all_rows}=    Get table data from a webpage
    # Action: Create result object from the headers and rows
    ${table}=    Create Table    ${all_rows}    columns=${headers}
    ${pandas_table}=    Evaluate    pandas.DataFrame(data=${all_rows}, columns=${headers})    modules=pandas
    Log To Console    RPA.Tables table:${table}
    Log To Console    pandas table:${pandas_table}
    Log    Done.



*** Keywords ***
Get table data from a webpage
    Open Available Browser    ${WEBSITE}    headless=True
    # Action: Collect header names for the table
    ${header_elements}=    Get WebElements    ${LOCATOR_TABLE_HEADINGS}
    ${headers}=    Create List
    FOR    ${h}    IN    @{header_elements}
        ${header_text}=    Evaluate    $h.text.strip()
        Append To List    ${headers}    ${header_text}
    END
    # Action: Loop table with pagination
    ${all_rows}=    Create List
    ${there_are_pages}=    Set Variable    ${TRUE}
    WHILE    ${there_are_pages}
        # Action: Collect rows from a single page in a table
        ${rows}=    Collect Table Rows
        ${all_rows}=    Combine Lists    ${all_rows}    ${rows}
        # Decision: Are the more pages to scrape ? Note. using the same variable as WHILE loop condition
        ${button_classes}=    Get Element Attribute    ${LOCATOR_NEXT_BUTTON}    class
        ${there_are_pages}=    Evaluate    "disabled" not in $button_classes
        # Action: Click next button to proceed to next page
        IF    ${there_are_pages}    Click Element    ${LOCATOR_NEXT_BUTTON}
    END
    Log To Console    headers:${headers}
    Log To Console    rows:${all_rows}
    RETURN    ${headers}    ${all_rows}

Collect Table Rows
    ${table_rows}=    Get WebElements    ${LOCATOR_TABLE_ROWS}
    ${rows}=    Create List
    FOR    ${row}    IN    @{table_rows}
        ${cells}=    Evaluate    $row.find_elements_by_tag_name("td")
        #${cell_contents}=    Evaluate    [c.text.strip() for c in $cells]
        ${cell_contents}=    Create List
        FOR    ${cell}    IN    @{cells}
            ${details}=    Get Details From Cell    ${cell}
            Append To List    ${cell_contents}    ${details}
        END
        Append To List    ${rows}    ${cell_contents}
    END
    RETURN    ${rows}

Get Details From Cell
    [Arguments]    ${cell}
    ${cell_text}=    Evaluate    $cell.text.strip()
    ${links}=    Evaluate    $cell.find_elements_by_tag_name("a")
    ${hrefs}=    Evaluate    [link.href for link in $links]
    ${details}=    Create Dictionary
    ...    text=${cell_text}
    ...    links=${hrefs}
    RETURN    ${details}
