*** Settings ***
Library           RPA.Email.ImapSmtp
Library           RPA.Robocorp.Vault

*** Variables ***
${BACKUP_FOLDER}    ${CURDIR}${/}backup

*** Keywords ***
Gmail authorization
    ${secrets}=    Get Secret    email
    Authorize    ${secrets}[username]    ${secrets}[password]    smtp.gmail.com    imap.gmail.com
    Log To Console    \nGmail access authorized

*** Tasks ***
Minimal task
    Gmail authorization
    ${messages}=    List Messages    SUBJECT "Testing!"    source_folder=The TESTING folder
    FOR    ${index}    ${msg}    IN ENUMERATE    @{messages}
        Log To Console    ${msg}[uid] - ${msg}[Subject]
        Save Messages    ${msg}    ${BACKUP_FOLDER}
        IF    $index % 2 == 0
            Move Messages    ${msg}    target_folder=custom name
        ELSE
            Delete Message    ${msg}
        END
    END
    Log    Done.
