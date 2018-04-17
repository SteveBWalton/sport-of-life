#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Module to run the sport of life program.
This is a little program to test console control under Linux and Windows.
'''

# System libraries.
import sys
import os
import argparse
import platform
import subprocess
import shutil
import datetime
import time

# Application Libraries.



if __name__ == '__main__':
    # Process the command line arguments.
    # This might end the program (--help).
    oParse = argparse.ArgumentParser(prog='sport_of_life', description='Little game to run under Linux and Windows.')
    oArgs = oParse.parse_args()

    # Welcome message.
    print('\033[1;31mSport Of Life\033[0;m by Steve Walton.')
    print('Python Version {}.{}.{} (expecting Python 3).'.format(sys.version_info.major, sys.version_info.minor, sys.version_info.micro))
    print('Operating System is "{}".  Desktop is "{}".'.format(platform.system(), os.environ.get('DESKTOP_SESSION')))

    for nCount in range(10):
        # This works on Windows but not in IDLE.
        print(nCount, end='\r', flush=True)

        # This does not work in Windows.
        # print(nCount)
        # sys.stdout.write("\033[F")

        # Wait for a second.
        time.sleep(1)
        

    # Main loop.

    print('Goodbye from the \033[1;31mSport Of Life\033[0;m program.')
