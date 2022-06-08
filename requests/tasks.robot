*** Settings ***
Library     ExtendedHTTPLibrary


*** Variables ***
${URL}      https://services-extest.ler.dk


*** Tasks ***
Minimal task
    Create Pkcs12 Session
    ...    LER
    ...    ${URL}
    ...    ${CURDIR}${/}FOCES_gyldig_2022.p12
    ...    Test1234
    ${response}=    GET On Session    LER    /api/SecureTest
    Log To Console    ${response}
    Log To Console    ${response.json()}
    Log    Done.
