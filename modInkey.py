#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Module to provide the BBC Basic function INKEY.
Scan for a keyboard button press but do not block if no key is available.
'''

import tty
import termios
import sys
import _thread
import time


try:
    # Try to import Windows version.
    from msvcrt import getch
except ImportError:
    # Define non-Windows version.
    def getch():
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            # print('SetRaw')
            # tty.setraw(sys.stdin.fileno())
            # print('SetCBreak')
            tty.setcbreak(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            # print('Restore termios')
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch



class CInKey:
    ''' Class to provide a keyboard scan function like BBC Basic InKey(). '''



    def __init__(self):
        ''' Class constructor. '''
        self.sLastKey = None
        _thread.start_new_thread(self._keypress, ())



    def _keypress(self):
        ''' Fetch the last character into a buffer. '''
        self.sLastKey = getch()



    def InKey(self):
        ''' Return the last (current) keypress or None for no keypress. '''
        if self.sLastKey == None:
            sReturn = None
        else:
            sReturn = self.sLastKey
            self.sLastKey = None
            _thread.start_new_thread(self._keypress, ())
        return sReturn



def main():
    oInKey = CInKey()
    while True:
        sCharacter = oInKey.InKey()
        if sCharacter == None:
            pass
            # print('No Key pressed.')
        else:
            print('"{}" key pressed.'.format(sCharacter))
            if sCharacter == 'q' or sCharacter == '\x1b':  # x1b is ESC
                break
        time.sleep(.5)



if __name__ == "__main__":
    print('Press \'q\' to finish.')
    main()
    print('Program finished')
