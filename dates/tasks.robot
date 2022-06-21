*** Settings ***
Library     DateLibrary
Library     Collections
Library     RPA.Excel.Files


*** Variables ***
@{MONTHS}=          04    05    06    07    08    09    10
${start_date}=      01/15/2000
${end_date}=        01/01/2022


*** Tasks ***
Minimal task
    ${now}=    Time Now    Europe/London
    ${diff}=    Time Difference    ${now}    22-06-09 04:56:30 PM    Europe/London
    Log To Console    ${diff}
    ${mytime}=    Create Datetime    18-05-2022 16:59    DD-MM-YYYY HH:mm    Europe/London
    ${diff}=    Time Difference    ${mytime}    ${now}
    FOR    ${month}    IN    @{MONTHS}
        ${dt}=    Create Datetime    05-${month}-22 12:00    DD-MM-YY HH:mm    Europe/London
        ${diff}=    Time Difference    ${dt}    ${now}
        IF    not ${diff}[end_date_is_greater]
            Log To Console    05-${month}-22 12:00 IS past current datetime (Europe/London)
            BREAK
        END
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

Parsing Entries from Excel
    Open Workbook    ${CURDIR}${/}dates.xlsx
    ${rows}=    Read Worksheet    header=True
    Run Keyword And Ignore Error    Create Worksheet    BeyondBusinessHours
    FOR    ${row}    IN    @{rows}
        ${entry_date}=    Create Datetime    ${row}[timestamp]
        ${diff}=    Time Difference    06/17/22 05:00 PM    ${entry_date}
        IF    ${diff}[end_date_is_greater]
            Append Rows To Worksheet    ${row}    name=BeyondBusinessHours    header=True
        END
    END
    Save Workbook

Getting previous business day
    # If public holidays are to be considered then country code needs
    # to be given for example.    FI is for Finland, IN for India
    ${business_day}=    Return Previous Business Day    06/27/22    FI
    # the Friday 24th of June is a public holiday in Finland
    # expected result is Thursday 23rd of June
    Should Be Equal In Days    ${business_day}    06/23/22
    ${formatted_business_day}=    Evaluate    $business_day.format("MM/DD/YY")
    Log to Console    ${formatted_business_day} 05:00:00 PM
