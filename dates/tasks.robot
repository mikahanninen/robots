*** Settings ***
Library     DateLibrary
Library     Collections


*** Variables ***
@{MONTHS}=          04    05    06    07    08    09    10
${start_date}=      01/15/2000
${end_date}=        01/01/2022


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

Getting months in between
    ${start_dt}=    Create Datetime    ${start_date}    MM/DD/YYYY
    ${start_dt}=    Evaluate    $start_dt.start_of('month')
    ${diff}=    Time Difference In Months    ${start_dt.month}/1/${start_dt.year}    ${end_date}
    @{months}=    Create List
    WHILE    ${diff}[months] > 0
        ${start_dt}=    Evaluate    $start_dt.add(months=1)
        ${diff}=    Time Difference In Months    ${start_dt}    ${end_date}
        IF    ${diff}[months]==0    BREAK
        Append To List    ${months}    ${start_dt.format('MM/DD/YYYY')}
    END
    Log To Console    \nFirst of months between ${start_date} and ${end_date}:\n@{months}
