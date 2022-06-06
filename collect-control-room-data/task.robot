*** Settings ***
Library     RPA.Robocorp.Process
Library     RPA.Robocorp.Vault


*** Tasks ***
Minimal Task
    ${secrets}=    Get Secret    control_room_process_acme
    Set Credentials
    ...    ${secrets}[workspace_id]
    ...    ${secrets}[process_id]
    ...    ${secrets}[api_key]
    ${items}=    List Process Work Items
    FOR    ${item}    IN    @{items}
        ${run}=    Get Process Run Status
        ...    process_run_id=${item}[processRunId]
        ...    step_run_id=${item}[activityRunId]
        Log To Console    ---------------------------------------
        Log To Console    Process Run ID: ${item}[processRunNo]
        Log To Console    Run Result: ${run}[result]
        Log To Console    Run Step ID: ${run}[stepId]
        Log To Console    Run Duration: ${run}[duration] sec
    END
