*** Settings ***
Library     RPA.Robocorp.Vault
Library     OracleExtendedDatabase


*** Tasks ***
Call Oracle's Stored Procedure
    ${secrets}=    Get Secret    Oracle
    Connect To Database    oracledb
    ...    database=${secrets}[db_name]
    ...    username=${secrets}[db_user]
    ...    password=${secrets}[db_pass]
    ...    host=${secrets}[db_address]
    @{params}=    Create List    Mika
    ${result}=    Oracle Call Procedure    PROCEDURE1    ${params}
    Log To Console    RESULT = ${result}
    Log To Console    Done.
