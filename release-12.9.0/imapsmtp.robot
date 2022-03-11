*** Settings ***
Library           RPA.Email.ImapSmtp
Library           RPA.Robocorp.Vault

*** Tasks ***
ImapSmtp Tasks
    Authorize ImapSmtp
    ${emails}    List Messages    BEFORE "23-OCT-2021"    INBOX
    FOR    ${email}    IN    @{emails}
        Log Message    ${email}
    END
    Send Email
    Log    Done.

*** Keywords ***
Log Message
    [Arguments]    ${msg}
    Log To Console    ${msg}[From] - ${msg}[Date]: ${msg}[Subject]

Authorize ImapSmtp
    ${secrets}=    Get Secret    email
    Authorize    ${secrets}[username]    ${secrets}[password]    smtp.gmail.com    imap.gmail.com

Send Email
    Send Message    robocorp.tester@gmail.com    mika@beissi.onmicrosoft.com
    ...    subject=Pretty New Test Email
    ...    body=bcc should be hidden NEW content of the message is really important
    ...    cc=robocorp.tester@gmail.com
    ...    bcc=mika.hanninen@gmail.com,robocorp.com
