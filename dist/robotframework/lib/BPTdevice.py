import time
from enum import Enum

from robot.utils import (ConnectionCache, abspath, cmdline2list, console_decode,
                         is_list_like, is_truthy, NormalizedDict, py2to3,
                         secs_to_timestr, system_decode, system_encode,
                         timestr_to_secs, IRONPYTHON, JYTHON, WINDOWS)
from robot.version import get_version
from robot.api import logger

import serial

from if_lib import bpt_if


class BptUartModes(Enum):
    '''BPT UART test modes.'''
    ECHO = 0
    ECHO_EXT = 1
    REG_ACCESS = 2
    TX = 3


class BPTdevice(bpt_if.BptIf):

    ROBOT_LIBRARY_SCOPE = 'TEST SUITE'
    ROBOT_LIBRARY_VERSION = get_version()

    def reset_dut(self):
        self.set_sys_cr(1)
        self.execute_changes()
        time.sleep(0.01)
        self.set_sys_cr(0)
        self.execute_changes()
        time.sleep(2)

    def setup_uart(self, mode=BptUartModes.ECHO.value, baudrate=115200,
                   parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE,
                   rts=True):
        '''Setup tester's UART.'''

        # setup testing mode
        cmd_info = self.set_uart_mode(int(mode))
        if cmd_info['result'] != 'Success':
            return False

        # setup baudrate
        cmd_info = self.set_uart_baud(int(baudrate))
        if cmd_info['result'] != 'Success':
            return False

        # setup UART control register
        ctrl = 0
        if parity == serial.PARITY_EVEN:
            ctrl = ctrl | 0x02
        elif parity == serial.PARITY_ODD:
            ctrl = ctrl | 0x04

        if stopbits == serial.STOPBITS_TWO:
            ctrl = ctrl | 0x01

        # invert RTS level as it is a low active signal
        if not rts:
            ctrl = ctrl | 0x08

        cmd_info = self.set_uart_ctrl(ctrl)
        if cmd_info['result'] != 'Success':
            return False

        # reset status register
        cmd_info = self.set_uart_status(0)
        if cmd_info['result'] != 'Success':
            return False

        # apply changes
        cmd_info = self.execute_changes()
        if cmd_info['result'] != 'Success':
            return False

        return True
