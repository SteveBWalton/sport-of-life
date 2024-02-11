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
    # print('Try to import Windows version')
    # import msvcrt
    from msvcrt import getwch # , kbhit
    # print('Using Windows getwch().')
    isLinux = False
except ImportError:
    # Define non-Windows version.
    # print('Using Linux getwch().')
    isLinux = True
    import tty
    import termios
    def getwch():
        fd = sys.stdin.fileno()
        global oldSettings
        oldSettings = termios.tcgetattr(fd)
        # print('tcgetattr({}) = {}'.format(fd, oldSettings))
        try:
            # This does not work !
            # print('SetRaw')
            # tty.setraw(sys.stdin.fileno())

            # print('\nSetCBreak\n')
            tty.setcbreak(sys.stdin.fileno())

            ch = sys.stdin.read(1)
        finally:
            # This use to work without the | termios.ECHO.
            # This does not work in the sport_of_life program for some reason.

            #print('tcgetattr({}) = {}'.format(fd, oldSettings))
            # print('tcgetattr({}) = {}'.format(fd, termios.tcgetattr(fd)))
            # print('\nRestore termios\n')
            oldSettings[3] = oldSettings[3] | termios.ECHO
            termios.tcsetattr(fd, termios.TCSADRAIN, oldSettings)
            # print('tcgetattr({}) = {}'.format(fd, termios.tcgetattr(fd)))

            # Use 'stty --all' to see all terminal settings.
            # Use 'stty echo' to turn echo back on (for example).
        return ch



class InKey:
    ''' Class to provide a keyboard scan function like BBC Basic InKey(). '''



    def __init__(self):
        ''' Class constructor. '''
        # print('CInKey class constructor.')
        self.lastKey = None
        # print('_thread.start_new_thread.')
        _thread.start_new_thread(self._keypress, ())
        # print('CInKey class constructor finished.')



    def __del__(self):
        ''' Class destructor. '''
        # print('InKey class destructor.')
        self.close()



    def close(self):
        ''' Restore the terminal. Sometimes there is an extra setcbreak() call.  So call here at the end to restore the ECHO after this setcbreak() call.'''
        # print('close')
        if isLinux:
            global oldSettings
            oldSettings[3] = oldSettings[3] | termios.ECHO
            fd = sys.stdin.fileno()
            termios.tcsetattr(fd, termios.TCSADRAIN, oldSettings)



    def _keypress(self):
        ''' Fetch the last character into a buffer. '''
        # print('_keypress().start')
        # if msvcrt.kbhit():
        # print('_keypress().start')
        # This does not work under minitty.
        # print ('_keypress.getwch()')
        self.lastKey = getwch()
        # print('_keypress().finish')



    def scanKey(self):
        ''' Return the last (current) keypress or None for no keypress. '''
        if self.lastKey == None:
            result = None
            # print('No Key pressed.')
        else:
            result = self.lastKey
            # print('"{}" key pressed.'.format(result))
            self.lastKey = None
            _thread.start_new_thread(self._keypress, ())
        return result



def main():
    # print('Hello from modInKey.py')
    inKey = InKey()
    # print('CInkey object created.')
    wait = 10000
    while wait > 0:
        character = inKey.scanKey()
        if character == None:
            pass
            print('No Key pressed.')
        else:
            print('"{}" key pressed.'.format(character))
            if character == 'q' or character == '\x1b':  # x1b is ESC
                break
                wait = 10
        time.sleep(1)
        wait -= 1

    time.sleep(1)
    time.sleep(1)
    time.sleep(1)
    time.sleep(1)
    time.sleep(1)
    inKey.close()



if __name__ == "__main__":
    print('Press \'q\' to finish.')
    main()
    print('Program finished')
