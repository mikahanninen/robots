*** Settings ***
Library     ExtendedWindows


*** Variables ***
${password}     32423keysy{lolsdad{}}}
${element}      name:"Text Editor"


*** Tasks ***
Minimal task
    Control Window    subname:Notepad
    Set Element Value    ${element}    \n{[{]{{][[{}]]}}}]}
    Set Element Value    ${element}    \n123123123    append=True
    Send Keys    ${element}    {CTRL}a
    Send Keys    ${element}    ${password}\n    raw=True
    Send Keys    ${element}    {[{]{{][[{}]]}}}]}\n    raw=True
    Send Keys    ${element}    123123123\n    raw=True
    Log    Done.
