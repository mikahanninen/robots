*** Settings ***
Library           RPA.Email.ImapSmtp
Library           RPA.Robocorp.Vault

*** Keywords ***
Gmail authorization
    ${secrets}=    Get Secret    email
    Authorize    ${secrets}[username]    ${secrets}[password]    smtp.gmail.com    imap.gmail.com
    Log To Console    \nGmail access authorized

*** Tasks ***
Minimal task
    Gmail authorization
    ${messages}=    List Messages    SUBJECT "Testing!"    source_folder=custom name
    FOR    ${index}    ${msg}    IN ENUMERATE    @{messages}
        Log To Console    ${msg}[uid] - ${msg}[Subject]
        IF    $index % 2 == 0
            Move Messages    ${msg}    target_folder=The TESTING folder
        ELSE
            Delete Message    ${msg}
        END
    END
    Log    Done.
