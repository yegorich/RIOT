*** Settings ***
Test Setup          Reset DUT and BPT

Library             OperatingSystem  
Library             UartDevice   port=%{PORT}        WITH NAME  UART
Library             BPTdevice   port=%{BPT_PORT}    WITH NAME  BPT

Resource            testutil.keywords.robot
Resource            expect.keywords.robot
Resource            periph.keywords.robot

Variables           test_vars.py

*** Test Cases ***
Echo Test
    ${result}=          UART.Init    1    115200
    Should Contain      ${result['result']}     Success
    ${result}=          BPT.Setup uart
    Should Be True      ${result}
    ${result}=          UART.Send     1    ${SHORT_TEST_STRING}
    Should Contain      ${result['data']}     ${SHORT_TEST_STRING}
    ${result}=          UART.Send     1    ${LONG_TEST_STRING}
    Should Contain      ${result['data']}     ${LONG_TEST_STRING}
    ${result}=          UART.Init    1    38400
    Should Contain      ${result['result']}     Success
    ${result}=          UART.Send     1    ${SHORT_TEST_STRING}
    Should Contain      ${result['result']}     Timeout

Extended Echo Test
    ${result}=          UART.Init    1    115200
    Should Contain      ${result['result']}     Success
    ${result}=          BPT.Setup uart     mode=1
    Should Be True      ${result}
    ${result}=          UART.Send     1    ${SHORT_TEST_STRING}
    Should Contain      ${result['data']}     ${SHORT_TEST_STRING_INC}
    ${result}=          UART.Send     1    ${LONG_TEST_STRING}
    Should Contain      ${result['data']}     ${LONG_TEST_STRING_INC}

Register Access Test
    ${result}=          UART.Init    1    115200
    Should Contain      ${result['result']}     Success
    ${result}=          BPT.Setup uart     mode=2
    Should Be True      ${result}
    ${result}=          UART.Send     1    ${REG_152_READ}
    Should Contain      ${result['data']}     ${REG_152_READ_DATA}
    ${result}=          UART.Send     1    ${REG_WRONG_READ}
    Should Be Equal     ${result['data']}     ${REG_WRONG_READ_DATA}
