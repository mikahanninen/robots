*** Settings ***
Library           RPA.Desktop

*** Tasks ***
Use Region as Locator
    # TODO. Open some app on Windows OS
    Click    alias:Button + region:0,0,300,800    double click
    Sleep    5s
    Click    alias:Button + region:300,0,800,800    double click
    Sleep    5s
    Log    Done.
