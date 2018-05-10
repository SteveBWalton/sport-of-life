#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Module to provide the BBC Basic function INKEY.
Scan for a keyboard button press but do not block if no key is available.
Under Windows.
    This works under winpty ( but colours do not work in winpty).
    This does not work under minitty.
'''

import sys
import _thread
import time


try:
    # Try to import Windows version.
    print('Try to import Windows version')
    # import msvcrt
    from msvcrt import getwch # , kbhit
    print('Using Windows getwch().')
except ImportError:
    # Define non-Windows version.
    import tty
    import termios
    def getwch():
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
        # print('CInKey class constructor.')
        self.sLastKey = None
        # print('_thread.start_new_thread.')
        _thread.start_new_thread(self._keypress, ())
        # print('CInKey class constructor finished.')

        

    def _keypress(self):
        ''' Fetch the last character into a buffer. '''
        # print('_keypress().start')
        # if msvcrt.kbhit():
        # print('_keypress().start')
        # This does not work under minitty.
        self.sLastKey = getwch()
        # print('_keypress().finish')



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
    # print('Hello from modInKey.py')
    oInKey = CInKey()
    # print('CInkey object created.')
    while True:
        sCharacter = oInKey.InKey()
        if sCharacter == None:
            pass
            print('No Key pressed.')
        else:
            print('"{}" key pressed.'.format(sCharacter))
            if sCharacter == 'q' or sCharacter == '\x1b':  # x1b is ESC
                break
        time.sleep(1)



if __name__ == "__main__":
    print('Press \'q\' to finish.')
    main()
    print('Program finished')
