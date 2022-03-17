*** Settings ***
Library           RPA.Browser.Selenium

*** Variables ***
@{URLS}
...               https://www.robocorp.com
...               https://docs.robocorp.com
...               https://portal.robocorp.com
...               https://suomi.fi

*** Tasks ***
Minimal task
    Attach Chrome Browser    9233
    Go To    https://portal.robocorp.com
    Wait Until Element Is Visible    //input[@id="q"]
    Input Text    //input[@id="q"]    windows
    Press Keys    ${NONE}    RETURN
    Log    Done.

*** Keywords ***
Loop Sites
    FOR    ${url}    IN    @{URLS}
        Go To    ${url}
        Sleep    10s
    END
