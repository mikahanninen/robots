*** Settings ***
Library     RPA.Browser.Selenium


*** Tasks ***
Options and Capabilities
    # Supporting links for different Chrome tweaking possibilities
    ## https://chromedriver.chromium.org/capabilities
    ## https://peter.sh/experiments/chromium-command-line-switches/
    ## https://developer.mozilla.org/en-US/docs/Web/API
    ## https://chromedevtools.github.io/devtools-protocol/
    ## ## https://chromedriver.chromium.org/
    ## NOTE. Selenium 4 provides better was of accessing Chrome's devtools
    ## https://www.selenium.dev/ja/documentation/webdriver/bidirectional/chrome_devtools/
    ## https://saucelabs.com/resources/articles/bidirectional-apis
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
    ${targets}=    Execute Cdp    Target.getTargets    ${TRUE}
    Log To Console    ${targets}
    Log    Done.
