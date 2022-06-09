*** Settings ***
Library     DateLibrary


*** Variables ***
@{MONTHS}=      04    05    06    07    08    09    10


*** Tasks ***
Minimal task
    ${now}=    Time Now    Europe/London
    ${diff}=    Time Difference    ${now}    22-06-09 04:56:30 PM
    Log To Console    ${diff}
    ${mytime}=    Create Datetime    18-05-2022 16:59    DD-MM-YYYY HH:mm    Europe/London
    ${diff}=    Time Difference    ${mytime}    ${now}
    FOR    ${month}    IN    @{MONTHS}
        ${dt}=    Create Datetime    05-${month}-22 12:00    DD-MM-YY HH:mm
        ${diff}=    Time Difference    ${dt}    ${now}
        IF    not ${diff}[end_date_is_greater]    BREAK
        Log To Console    05-${month}-22 12:00 is not past current datetime (Europe/London)
    END

    Log    Done.
