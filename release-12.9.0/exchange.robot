*** Settings ***
Library           RPA.Email.Exchange
Library           RPA.Robocorp.Vault

*** Tasks ***
Exchange List Messages
    [Setup]    Authorize Exchange
    List Exchange Messages
    Log    Done.

Exchange Filter Messages With Different Filters
    [Setup]    Authorize Exchange
    Using advanced criteria
    Log    Done.

Exchange Wait For Messages
    [Setup]    Authorize Exchange
    Wait For It
    Log    Done.

Exchange Wait For Message by Sender
    [Setup]    Authorize Exchange
    Wait For Sender
    Log    Done.

*** Keywords ***
List Exchange Messages
    ${messages}=    List Messages    criterion=after:31-12-2021
    FOR    ${m}    IN    @{messages}
        IF    $m["has_attachments"]
            Log To Console    Email '${m}[subject]' has attachments
        ELSE
            Log To Console    Email '${m}[subject]' does NOT have attachments
        END
    END

Wait For It
    ${messages}=    Wait For Message
    ...    criterion=sender_contains:robocorp.tester@gmail.com subject:epic after:NOW
    ...    timeout=60
    IF    len($messages) == 0
        Log To Console    DID NOT RECEIVE THE EXPECTED MESSAGE
    ELSE
        FOR    ${msg}    IN    @{messages}
            Log Message    ${msg}
        END
    END

Wait For Sender
    ${messages}=    Wait For Message
    ...    criterion=sender_contains:robocorp.tester@gmail.com after:NOW
    ...    timeout=60
    IF    len($messages) == 0
        Log To Console    DID NOT RECEIVE THE EXPECTED MESSAGE
    ELSE
        FOR    ${msg}    IN    @{messages}
            Log Message    ${msg}
        END
    END

Using advanced criteria
    Log To Console    \nUsing Advanced Criteria
    Log To Console    Check 1
    ${messages}=    List Messages
    ...    criterion=between:'08-03-2022 and 10-03-2022 23:00' subject_contains:'Message center'
    FOR    ${msg}    IN    @{messages}
        Log Message    ${msg}
    END
    Log To Console    Check 2
    ${messages}=    List Messages
    ...    criterion=between:'08-03-2022 and 10-03-2022 23:00' body_contains:'Dynamic Distribution Groups'
    FOR    ${msg}    IN    @{messages}
        Log Message    ${msg}
    END
    Log To Console    Check 3
    ${messages}=    List Messages
    ...    criterion=category:'Green category' subject_contains:Message center
    FOR    ${msg}    IN    @{messages}
        Log Message    ${msg}
    END
    Log To Console    Check 4
    ${messages}=    List Messages
    ...    criterion=category:'Green category' importance:high
    FOR    ${msg}    IN    @{messages}
        Log Message    ${msg}
    END
    Log To Console    Check 5
    ${messages}=    List Messages
    ...    criterion=sender_contains:mika@robocorp.com
    FOR    ${msg}    IN    @{messages}
        Log Message    ${msg}
    END

Log Message
    [Arguments]    ${msg}
    Log To Console    ${msg}[sender][email_address] - ${msg}[datetime_received]: ${msg}[subject]

Authorize Exchange
    [Arguments]    ${use_primary_smtp_address}=${FALSE}
    ${secret}=    Get Secret    Exchange
    IF    ${use_primary_smtp_address}
        Authorize
        ...    username=${secret}[account]
        ...    password=${secret}[password]
        ...    autodiscover=False
        ...    server=outlook.office365.com
        ...    primary_smtp_address=${secret}[shared_mailbox]
    ELSE
        Authorize
        ...    username=${secret}[account]
        ...    password=${secret}[password]
        ...    autodiscover=False
        ...    server=outlook.office365.com
    END
