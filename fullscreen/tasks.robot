*** Settings ***
Library             RPA.Browser.Playwright    WITH NAME    PW
Library             RPA.Browser.Selenium    WITH NAME    SL
Library             RPA.Desktop    WITH NAME    D
Library             ExtendedSelenium    WITH NAME    ESL

Suite Teardown      SL.Close All Browsers


*** Variables ***
${WEBSITE}      https://portal.robocorp.com


*** Tasks ***
Selenium Full Page Screenshot
    SL.Open Browser    ${WEBSITE}    options=add_argument("--headless")
    SL.Capture Page Screenshot    filename=SL-page.png
    Selenium Set Window Size
    SL.Capture Page Screenshot    filename=SL-page-after-scroll.png

Playwright Full Page Screenshot
    PW.New Browser    chromium
    PW.New Page    ${WEBSITE}
    PW.Take Screenshot    filename=%{ROBOT_ARTIFACTS}${/}PW-page    fullPage=True

Selenium Chrome Zooming
    SL.Open Available Browser    ${WEBSITE}    browser_selection=chrome
    @{zoomlevels}=    Create List    20    50    150    200
    FOR    ${zoomlevel}    IN    @{zoomlevels}
        SL.Execute Javascript    document.body.style.zoom='${zoomlevel}%'
        Sleep    5s
    END

Selenium Firefox Zooming
    ESL.Open Available Browser    ${WEBSITE}    browser_selection=firefox
    Repeat Keyword    5 times    ESL.Firefox Mac Zoom Out
    Sleep    5s
    [Teardown]    ESL.Close All Browsers


*** Keywords ***
Selenium Set Window Size
    ${screen_width}=    SL.Execute Javascript    return document.body.parentNode.scrollWidth
    ${screen_height}=    SL.Execute Javascript    return document.body.parentNode.scrollHeight
    SL.Set Window Size    ${screen_width}    ${screen_height}
    Sleep    0.5
