*** Settings ***
Library           RPA.Browser.Selenium
Library           RPA.Desktop

*** Tasks ***
Use Region as Locator
    [Teardown]    Close All Browsers
    Open Available Browser    file://%{ROBOT_ROOT}${/}page.html
    Maximize Browser Window
    Click    alias:Button + region:0,0,300,800    double click
    Sleep    5s
    ${location}=    Get Location
    Log To Console    Page location: ${location}
    Go To    file://%{ROBOT_ROOT}${/}page.html
    Click    alias:Button + region:300,0,800,800    double click
    Sleep    5s
    ${location}=    Get Location
    Log To Console    Page location: ${location}
    Log    Done.
