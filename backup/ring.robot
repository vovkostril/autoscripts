*** Settings ***
Library  ring.ITU_T_G_8032

*** Variables ***


*** Test Cases ***
Save starting configs
    # Skip
    ${flash}=  make_backups
    Should Contain    ${flash}    

Cleanup
    # Skip
    ${value}=  cleanup
    Should Be Equal    ${value}    Done

Serial
    # Skip
    ${value}=  open_serials
    Should Be Equal    ${value}    serial connection found

Configure 
    # Skip
    ${erps}=  configure
    ${logs}=  get_logs
    Log    ${logs}[0]
    Log    ${logs}[1]
    Log    ${logs}[2]
    Log    ${logs}[3]
    Log    ${logs}[4]
    Log    ${logs}[5]
    Log    ${logs}[6]
    Should Be Equal    ${erps}    Done

Test 1: Testing that works
    # Skip
    ${value}=  test_one
    ${logs}=  get_logs
    Log    ${logs}[0]
    Log    ${logs}[1]
    Log    ${logs}[2]
    Log    ${logs}[3]
    Log    ${logs}[4]
    Log    ${logs}[5]
    Log    ${logs}[6]
    Should Be Equal    ${value}    Passed

Test 2: Port Shutdown
    # Skip
    ${value}=  test_two
    ${logs}=  get_logs
    Log    ${logs}[0]
    Log    ${logs}[1]
    Log    ${logs}[2]
    Log    ${logs}[3]
    Log    ${logs}[4]
    Log    ${logs}[5]
    Log    ${logs}[6]
    Should Be Equal    ${value}    Passed

Test 3: Reload 
    # Skip
    ${value}=  test_three
    ${logs}=  get_logs
    Log    ${logs}[0]
    Log    ${logs}[1]
    Log    ${logs}[2]
    Log    ${logs}[3]
    Log    ${logs}[4]
    Log    ${logs}[5]
    Log    ${logs}[6]
    Should Be Equal    ${value}    Passed

Load starting configs
    # Skip
    ${flash}=  load_backups
    Should Not Contain    ${flash}    

Close serial
    # Skip
    ${value}=  close_serials
    Should Be Equal    ${value}    Done

