*** Settings ***
Library     RPA.Browser.Selenium


*** Tasks ***
Robot Framework Example
    Open Available Browser    https://docs.robocorp.com
    Set Window Name    MAIN_TAB
    Keyword Which Opens New Window or Tab
    ...    https://portal.robocorp.com
    ...    PORTAL_TAB
    Keyword Which Opens New Window or Tab
    ...    https://github.com/robocorp/rpaframework
    ...    LIBRARY_REPOSITORY
    ...    window=${TRUE}
    # Now using the named windows/tabs
    Switch Window    ${MAIN_TAB}    # Using named handle stored as a variable
    Sleep    5s
    Switch Window    ${LIBRARY_REPOSITORY}    # Using named handle stored as a variable
    Sleep    5s
    Switch Window    ${PORTAL_TAB}    # Using named handle stored as a variable
    Sleep    5s
    Log    Done.


*** Keywords ***
Set Window Name
    [Documentation]    Set window name for current window/tab
    [Arguments]    ${window_variable_name}
    ${handles}=    Get Window Handles
    Set Global Variable    ${${window_variable_name}}    ${handles}[-1]
    Log To Console    ${SELENIUM_WINDOW_LIST}

Keyword Which Opens New Window or Tab
    [Arguments]    ${url}    ${window_variable_name}    ${window}=${FALSE}
    ${previous_handles}=    Get Window Handles
    IF    ${window}
        Execute Javascript    window.open('${url}', '_blank', 'height=800,width=600');
    ELSE
        Execute Javascript    window.open('${url}');
    END
    FOR    ${_}    IN RANGE    10
        ${handles}=    Get Window Handles
        IF    len($handles) > len($previous_handles)
            Set Window Name    ${window_variable_name}
            RETURN
        END
        Sleep    0.2s
    END
    Log    Was NOT able to detect new window in Selenium context    level=WARN
