*** Settings ***
Library     utils.py


*** Tasks ***
Minimal task
    HTML2PDF    ${CURDIR}${/}example.html    ${CURDIR}${/}example.pdf
    Log    Done.
