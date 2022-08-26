*** Settings ***
Library     RPA.Browser.Selenium


*** Tasks ***
Minimal task
    # https://chromedriver.chromium.org/capabilities
    # https://peter.sh/experiments/chromium-command-line-switches/
    ${options}=    Evaluate    selenium.webdriver.ChromeOptions()    modules=selenium.webdriver
    ${original_caps}=    Evaluate
    ...    selenium.webdriver.DesiredCapabilities.CHROME.copy()
    ...    modules=selenium.webdriver
    Log To Console    ${original_caps}
    Evaluate    $options.add_argument("start-fullscreen")
    Open Browser    https://portal.robocorp.com/    browser=chrome    options=${options}
    ${caps}=    Evaluate    $options.to_capabilities()
    Sleep    5s
    Open Browser    https://robocorp.com/    browser=chrome    desired_capabilities=${caps}
    Log    Done.
