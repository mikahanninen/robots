*** Settings ***
Library           RPA.Robocorp.WorkItems
Library           SharepointLibrary

*** Keywords ***
Handle Issue
    ${mail} =    Get Work Item Variable    parsedEmail
    &{issue}=    Get Sharepoint Issue From Email Body    ${mail}[Body]
    FOR    ${key}    IN    @{issue.keys()}
        Log    ${key}: ${issue}[${key}]
    END

*** Tasks ***
Power Automating
    For Each Input Work Item    Handle Issue
