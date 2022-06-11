*** Settings ***
Library     ExtendedDesktopWindows
Library     utils.py


*** Variables ***
${password}     32423keysy {lolsdad{}}}
${element}      Text Editor


*** Tasks ***
Minimal task
    Open Dialog    Notepad    wildcard=True
    Send Keys    ^a
    ${raw}=    Get Raw Keys    ${password}
    Type Into    ${element}    ${raw}
    Send Keys    ^a
    Type Into    ${element}    ${password}    raw=True
    Log    Done.
