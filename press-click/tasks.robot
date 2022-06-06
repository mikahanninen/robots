*** Settings ***
Library     RPA.Windows    WITH NAME    Windows
Library     ExtendedDesktop    WITH NAME    Desktop


*** Tasks ***
Minimal task
    Control Window    subname:"Visual Studio Code"
    ${elements}=    Get Elements    type:Tree and name:"Files Explorer" and depth:24 > type:TreeItem
    Shift Select Set of Files    ${elements}
    Sleep    5s
    Control Select Set of Files    ${elements}


*** Keywords ***
Control Select Set of Files
    [Arguments]    ${elements}
    ${selections}=    Create List    tasks.robot    conda.yaml    robot.yaml
    Press Key    ctrl
    Select Matching Names In Elements    ${elements}    ${selections}
    [Teardown]    Release Key    ctrl

Shift Select Set of Files
    [Arguments]    ${elements}
    ${selections}=    Create List    conda.yaml    tasks.robot
    Press Key    shift
    Select Matching Names In Elements    ${elements}    ${selections}
    [Teardown]    Release Key    shift

Click Windows Element Center
    [Arguments]    ${element}
    ${locator}=    Set Variable    coordinates:${element.xcenter},${element.ycenter}
    Desktop.Click    ${locator}

Select Matching Names In Elements
    [Arguments]    ${elements}    ${selections}
    FOR    ${elem}    IN    @{elements}
        IF    "${elem.name}" in ${selections}
            Click Windows Element Center    ${elem}
        END
    END
