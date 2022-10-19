*** Settings ***
Documentation       Task containing three steps. If both steps 1 and 2 fail then step 3
...                 is not run at all.
...                 \n*NOTE.* Keyword "Fail" is just used for simulating errors in the task execution

Library             Collections

Task Setup          Set Environment
Task Teardown       Cleanup Environment


*** Tasks ***
Minimal task
    TRY
        ${status1}=    Step 1
        ${status2}=    Step 2
        IF    not $status1 and not $status2
            Log    Step 1 and Step 2 both failed, not running Step 3    level=WARN
        ELSE
            # the status of step3 is not stored, as this example is not using it
            Step 3
        END
    EXCEPT
        ${error_message}=    Set Variable    Unknown error situation. We should not end up in here.
        Append To List    ${BOT_STATE}[errors]    ${error_message}
        Log    ${error_message}    level=ERROR
        Fail
    END
    Log    Done.


*** Keywords ***
Set Environment
    [Documentation]    Keyword that sets everything necessary for the bot
    &{state}=    Create Dictionary    running=${TRUE}    errors=@{EMPTY}
    Set Global Variable    ${BOT_STATE}    ${state}
    Log To Console    ${BOT_STATE}

Cleanup Environment
    [Documentation]    Keyword that clears the environment after the execution
    Set To Dictionary    ${BOT_STATE}    running=${FALSE}
    IF    ${BOT_STATE}[errors]
        Log    ERROR DURING BOT EXECUTION:\n${{'\n'.join($BOT_STATE['errors'])}}    level=WARN
    END
    Log To Console    ${BOT_STATE}

Step 1
    [Documentation]    Business logic part 1
    Log To Console    Running step 1
    TRY
        # 50% chance of failure
        IF    ${{random.randint(1,2)==1}}    Fail
    EXCEPT
        Append To List    ${BOT_STATE}[errors]    FAIL: Step 1
        RETURN    ${FALSE}
    END
    RETURN    ${TRUE}

Step 2
    [Documentation]    Business logic part 2
    Log To Console    Running step 2
    TRY
        # 50% chance of failure
        IF    ${{random.randint(1,2)==1}}    Fail
    EXCEPT
        Append To List    ${BOT_STATE}[errors]    FAIL: Step 2
        RETURN    ${FALSE}
    END
    RETURN    ${TRUE}

Step 3
    [Documentation]    Business logic part 3
    Log To Console    Running step 3
    TRY
        # 33% chance of failure
        IF    ${{random.randint(1,3)==1}}    Fail
    EXCEPT
        Append To List    ${BOT_STATE}[errors]    FAIL: Step 3
        RETURN    ${FALSE}
    END
    # 33% chance of generating an error which should not be happening
    IF    ${{random.randint(1,3)==1}}    Fail
    RETURN    ${TRUE}
