*** Settings ***
Library     RPA.Browser.Selenium
Library     OperatingSystem
Library     RPA.JSON


*** Tasks ***
Performance measurement in Incognito mode
    ${options}=    Evaluate    selenium.webdriver.ChromeOptions()    modules=selenium.webdriver
    Evaluate    $options.add_argument("incognito")
    Evaluate    $options.set_capability("goog:loggingPrefs", {'performance': 'ALL'})
    Open Browser    about:blank    browser=chrome    options=${options}
    Execute Javascript    performance.mark("Begin")
    Go To    https://robocorp.com/
    Click Element    //a[@href="https://robocorp.com/contact-us"]
    Execute Javascript    performance.mark("End")
    ${metrics}=    Execute Javascript    return window.performance.getEntries("mark")
    Save JSON to file    ${metrics}    metrics.json
    FOR    ${entry}    IN    @{metrics}
        Log To Console    ----------
        Log To Console    name = ${entry}[name]
        Log To Console    startTime = ${entry}[startTime]
        Log To Console    duration = ${entry}[duration]
    END
    Log    Done.
