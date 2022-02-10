*** Settings ***
Library           RPA.Email.ImapSmtp
Library           RPA.Robocorp.Vault

*** Variables ***
${BACKUP_FOLDER}    ${CURDIR}${/}backup
${ATTACHMENT_FOLDER}    ${CURDIR}${/}attachments

*** Keywords ***
Gmail authorization
    ${secrets}=    Get Secret    email
    Authorize    ${secrets}[username]    ${secrets}[password]    smtp.gmail.com    imap.gmail.com
    Log To Console    \nGmail access authorized

*** Tasks ***
Minimal task
    Gmail authorization
    ${messages}=    List Messages    SUBJECT "Message from Robot"    source_folder=The TESTING folder
    FOR    ${index}    ${msg}    IN ENUMERATE    @{messages}
        Log To Console    ${msg}[uid] - ${msg}[Subject]
        # Save message as .eml to BACKUP_FOLDER and attachments to ATTACHMENT_FOLDER
        Save Messages    ${msg}    ${BACKUP_FOLDER}    prefix=saved_message_
        Save Attachment
        ...    ${msg}
        ...    ${ATTACHMENT_FOLDER}
        ...    overwrite=${TRUE}
        ...    prefix=message_${msg}[uid]_
        # Move half and delete half
        IF    $index % 2 == 0
            Move Messages    ${msg}    target_folder=custom name
        ELSE
            Delete Message    ${msg}
        END
    END
    Log    Done.
