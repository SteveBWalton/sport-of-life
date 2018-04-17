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
        print('{:>20} {:>2} - {:<2} {:<20}'.format(oPlayer1.NameWithRanking(), nScore1, nScore2, oPlayer2.NameWithRanking()), end='\r', flush=True)

        # Wait.
        time.sleep(0.25)

    print()

    # Return the winner and loser.
    if nScore1 > nScore2:
        return oPlayer1, oPlayer2
    return oPlayer2, oPlayer1



def PlayRound(oPlayers, nKeyHome, nKeyAway, nKeyWin, nKeyLose, nNumMatches, nScore):
    ''' Play a round of a tournament. '''
    for nMatch in range(nNumMatches):
        nPlayer1 = random.randint(0, len(oPlayers)-1)
        while oPlayers[nPlayer1].round != nKeyHome:
            nPlayer1 = random.randint(0, len(oPlayers)-1)
        oPlayers[nPlayer1].round = nKeyWin

        nPlayer2 = random.randint(0, len(oPlayers)-1)
        while oPlayers[nPlayer2].round != nKeyHome:
            nPlayer2 = random.randint(0, len(oPlayers)-1)
        oPlayers[nPlayer2].round = nKeyWin

        oWinner, oLoser = PlayMatch(oPlayers[nPlayer1], oPlayers[nPlayer2], nScore)
        oLoser.round = nKeyLose

        
        
def PlayTournament(oPlayers):
    ''' Play a tournament with all the players. '''
    for oPlayer in oPlayers:
        oPlayer.round = 1

    # Round One.
    print('Round One')
    PlayRound(oPlayers, 1, 1, 2, -1, 16, 10)

    # Round Two.
    print('Round Two')
    PlayRound(oPlayers, 2, 2, 3, -2, 8, 13)

    # Quarter Finals.
    print('Quarter Finals')
    PlayRound(oPlayers, 3, 3, 4, -3, 4, 13)

    # Semi Finals.
    print('Semi Finals')
    PlayRound(oPlayers, 4, 4, 5, -4, 2, 17)

    print('Final')
    PlayRound(oPlayers, 5, 5, -6, -5, 1, 18)

    # Allocate ranking points.
    for oPlayer in oPlayers:
        nPts = [0, 1, 2, 4, 8, 16, 32][-oPlayer.round]
        oPlayer.history.append(nPts)
        while len(oPlayer.history) > 3:
            del oPlayer.history[0]
        oPlayer.pts = 0 
        for nPts in oPlayer.history:
            oPlayer.pts += nPts
    
    
    
def ShowRanking(oPlayers, bUpdate):
    ''' Display the players in ranking points order. '''
    # Sort by pts.
    oPlayers = sorted(oPlayers, key=lambda CPlayer: CPlayer.pts, reverse=True)
    # oPlayers = sorted(oPlayers, key=attrgetter('pts'), reverse=True)
    
    print('Top 10')
    nCount = 1
    for oPlayer in oPlayers: 
        if nCount <= 10:
            print('{:>5} {:<20}{:>4}'.format(nCount, oPlayer.NameWithRanking(), oPlayer.pts), end='')
            for nPts in oPlayer.history:
                print('{:>3}'.format(nPts), end='')
            print()   
        if bUpdate:
            oPlayer.ranking = nCount
        nCount = nCount + 1

        
    
def Run():
    ''' Execute the sport of life game. '''
    oPlayers = []
    for nLoop in range(32):
        oPlayer = modPlayer.CPlayer(None)
        oPlayer.name = 'Player {}'.format(nLoop+1)
        oPlayer.skill = random.randint(100, 999)
        oPlayers.append(oPlayer)

    PlayTournament(oPlayers)
    ShowRanking(oPlayers, True)
    
    PlayTournament(oPlayers)
    ShowRanking(oPlayers, True)

    PlayTournament(oPlayers)
    ShowRanking(oPlayers, True)

    PlayTournament(oPlayers)
    ShowRanking(oPlayers, True)


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
