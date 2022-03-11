*** Settings ***
Library           RPA.Desktop.Windows

*** Tasks ***
Windows Tasks
    ${result}=    Open using run dialog    calc.exe    Calculator
    ${_}    ${elements}=    Get Window Elements
    FOR    ${elem}    IN    @{elements}
        Log To Console    ${elem}
    END
