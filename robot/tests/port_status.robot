*** Settings ***
Library    ../keywords/port_keywords.py
*** Variables ***

*** Test Cases ***
Port 1 Should Be Connected Offline
    [Tags]    offline
    ${status}=    Get Port Status    1    file
    Should Be Equal    ${status}    connected

Port 10 Should Be Not Connected Offline
    [Tags]    offline
    ${status}=    Get Port Status    10    file
    Should Be Equal    ${status}    notconnect

Port 1 Should Be Connected Online
    ${status}=    Get Port Status    1    switch
    Should Be Equal    ${status}    connected

Port 10 Should Be Not Connected Online
    ${status}=    Get Port Status    10    switch
    Should Be Equal    ${status}    notconnect
