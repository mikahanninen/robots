*** Settings ***
Library     RPA.Windows
Library     EdgeLibrary    WITH NAME    Browser
Library     Process


*** Variables ***
${REMOTE_PORT}      9222


*** Tasks ***
Minimal task
    Log To Console    \nRemember: start msedge.exe --remote-debugging-port\=${REMOTE_PORT}
    # Using `RPA.Windows.Control Window` keyword to bring Edge to the foreground
    Control Window    executable:msedge.exe
    Attach Edge Browser    ${REMOTE_PORT}
    Go To    https://portal.robocorp.com
    Input Text When Element Is Visible    //input[@id="q"]    browser
    Click Element    //button[@type="submit"]
    # Wait before taking screenshot
    Sleep    5s
    Browser.Screenshot    filename=screenshot.png
    Log    Done.
