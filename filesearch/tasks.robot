*** Settings ***
Library         utils.py
Variables       testdata.py


*** Tasks ***
Minimal task
    Log To Console    \n\nFinding text in set of files defined in the testdata.py\n
    FOR    ${data}    IN    @{TESTDATA}
        ${found}=    Find In File    ${data}[0]    ${data}[1]
        Log To Console    Did we find "${data}[1]" in the file ${data}[0] [${{"YES" if $found else "NO"}}]
    END
    Log    Done.
