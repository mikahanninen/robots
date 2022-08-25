*** Settings ***
Library     ExtendedProcess
Library     RPA.Robocorp.Vault
Library     RPA.HTTP
Library     OperatingSystem


*** Tasks ***
Downloading Artifact Files From Control Room
    ${secrets}=    Get Secret    control_room_process
    Set Credentials
    ...    ${secrets}[workspace_id]
    ...    ${secrets}[process_id]
    ...    ${secrets}[api_key]
    ${items}=    List Process Work Items
    FOR    ${item}    IN    @{items}
        # Get process run details
        ${run}=    Get Process Run Status
        ...    process_run_id=${item}[processRunId]
        ...    step_run_id=${item}[activityRunId]
        Log To Console    ---------------------------------------
        Log To Console    Process Run ID: ${item}[processRunNo]
        Log To Console    Run Result: ${run}[result]
        Log To Console    Run Step ID: ${run}[stepId]
        Log To Console    Run Duration: ${run}[duration] sec
        # List robot run artifacts
        ${artifacts}=    List Run Artifacts
        ...    process_run_id=${item}[processRunId]
        ...    step_run_id=${item}[activityRunId]
        FOR    ${artifact}    IN    @{artifacts}
            Log To Console    ${artifact}
            # Download all .xlsx artifact files
            IF    ".xlsx" in "${artifact}[fileName]"
                ${download_link}=    Get Robot Run Artifact
                ...    process_run_id=${item}[processRunId]
                ...    step_run_id=${item}[activityRunId]
                ...    artifact_id=${artifact}[id]
                ...    filename=${artifact}[fileName]
                Download
                ...    ${download_link}
                ...    target_file=%{ROBOT_ARTIFACTS}${/}run_${item}[processRunNo]_${artifact}[fileName]
                ...    overwrite=${TRUE}
                ...    stream=${TRUE}
            END
        END
    END
