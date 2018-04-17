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
import random

# Application Libraries.
import modPlayer



def PlayMatch(oPlayer1, oPlayer2, nWin):
    ''' Play a match between the specified players. '''
    nScore1 = 0
    nScore2 = 0
    while nScore1 < nWin and nScore2 < nWin:
        if random.randrange(oPlayer1.skill) >= random.randrange(oPlayer2.skill):
            nScore1 += 1
        else:
            nScore2 += 1
        print('{:>20} {:>2} - {:<2} {:<20}'.format(oPlayer1.name, nScore1, nScore2, oPlayer2.name), end='\r', flush=True)

        # Wait.
        time.sleep(0.5)

    print()

    # Return the winner and loser.
    if nScore1 > nScore2:
        return oPlayer1, oPlayer2
    return oPlayer2, oPlayer1



def PlayRound(oPlayers, nKey, nNumMatches, nScore):
    ''' Play a round of a tournament. '''
    for nMatch in range(nNumMatches):
        nPlayer1 = random.randint(0, len(oPlayers)-1)
        while oPlayers[nPlayer1].round != nKey:
            nPlayer1 = random.randint(0, len(oPlayers)-1)
        oPlayers[nPlayer1].round = nKey+1

        nPlayer2 = random.randint(0, len(oPlayers)-1)
        while oPlayers[nPlayer2].round != nKey:
            nPlayer2 = random.randint(0, len(oPlayers)-1)
        oPlayers[nPlayer2].round = nKey+1

        oWinner, oLoser = PlayMatch(oPlayers[nPlayer1], oPlayers[nPlayer2], nScore)
        oLoser.round = 0



def Run():
    ''' Execute the sport of life game. '''
    oPlayer1 = modPlayer.CPlayer(None)
    oPlayer2 = modPlayer.CPlayer(None)
    oPlayer1.name = "Steve Davis"
    oPlayer1.skill = 550
    oPlayer2.name = "Stephen Hendry"
    oPlayers = []
    for nLoop in range(16):
        oPlayer = modPlayer.CPlayer(None)
        oPlayer.name = 'Player {}'.format(nLoop)
        oPlayer.skill = random.randint(100, 999)
        oPlayer.round = 1
        oPlayers.append(oPlayer)

    # Round One.
    print('Round One')
    PlayRound(oPlayers, 1, 8, 10)
    #for nMatch in range(8):
    #    nPlayer1 = random.randint(0, len(oPlayers)-1)
    #    while oPlayers[nPlayer1].round != 1:
    #        nPlayer1 = random.randint(0, len(oPlayers)-1)
    #    oPlayers[nPlayer1].round = 2
    #
    #    nPlayer2 = random.randint(0, len(oPlayers)-1)
    #    while oPlayers[nPlayer2].round != 1:
    #        nPlayer2 = random.randint(0, len(oPlayers)-1)
    #    oPlayers[nPlayer2].round = 2
    #
    #    oWinner, oLoser = PlayMatch(oPlayers[nPlayer1], oPlayers[nPlayer2], 10)
    #    oLoser.round = 0

    # Quarter Finals.
    print('Quarter Finals')
    PlayRound(oPlayers, 2, 4, 13)
    #for nMatch in range(4):
    #    nPlayer1 = random.randint(0, len(oPlayers)-1)
    #    while oPlayers[nPlayer1].round != 2:
    #        nPlayer1 = random.randint(0, len(oPlayers)-1)
    #    oPlayers[nPlayer1].round = 3
    #
    #    nPlayer2 = random.randint(0, len(oPlayers)-1)
    #    while oPlayers[nPlayer2].round != 2:
    #        nPlayer2 = random.randint(0, len(oPlayers)-1)
    #    oPlayers[nPlayer2].round = 3
    #
    #    oWinner, oLoser = PlayMatch(oPlayers[nPlayer1], oPlayers[nPlayer2], 10)
    #    oLoser.round = 0

    # Semi Finals.
    print('Semi Finals')
    PlayRound(oPlayers, 3, 2, 17)

    print('Final')
    PlayRound(oPlayers, 4, 1, 18)


if __name__ == '__main__':
    # Process the command line arguments.
    # This might end the program (--help).
    oParse = argparse.ArgumentParser(prog='sport_of_life', description='Little game to run under Linux and Windows.')
    oArgs = oParse.parse_args()

    # Welcome message.
    print('\033[1;31mSport Of Life\033[0;m by Steve Walton.')
    print('Python Version {}.{}.{} (expecting Python 3).'.format(sys.version_info.major, sys.version_info.minor, sys.version_info.micro))
    print('Operating System is "{}".  Desktop is "{}".'.format(platform.system(), os.environ.get('DESKTOP_SESSION')))

    #for nCount in range(10):
    #    # This works on Windows but not in IDLE.
    #    print(nCount, end='\r', flush=True)
    #
    #    # This does not work in Windows.
    #    # print(nCount)
    #    # sys.stdout.write("\033[F")
    #
    #    # Wait for a second.
    #    time.sleep(1)

    # Main loop.
    Run()

    print('Goodbye from the \033[1;31mSport Of Life\033[0;m program.')
