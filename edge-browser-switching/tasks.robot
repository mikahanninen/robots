*** Settings ***
Library           RPA.Browser.Selenium
Library           RPA.Desktop

*** Tasks ***
Switch to new Window on Edge browser
    [Teardown]    Close All Browsers
    Set Screenshot Directory    ${CURDIR}${/}output
    Open Browser    file://%{ROBOT_ROOT}${/}page.html    edge
    Wait Until Element is Visible    id:link
    Capture Page Screenshot
    Click Element    id:link
    ${handles}=    Get Window Handles
    Switch Window    ${handles}[-1]
    Wait Until Element Is Visible    //input[@id="q"]
    Capture Page Screenshot
    Log    Done.
