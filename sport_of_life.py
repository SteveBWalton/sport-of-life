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
        print('{:>22} {:>2} - {:<2} {:<22}'.format(oPlayer1.NameWithRanking(), nScore1, nScore2, oPlayer2.NameWithRanking()), end='\r', flush=True)

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
        # Find 2 players that are in this round.
        nPlayer1 = random.randint(0, len(oPlayers)-1)
        while oPlayers[nPlayer1].round != nKeyHome:
            nPlayer1 = random.randint(0, len(oPlayers)-1)
            # print('{} {}'.format(nPlayer1, oPlayers[nPlayer1].round))
        oPlayers[nPlayer1].round = nKeyWin

        nPlayer2 = random.randint(0, len(oPlayers)-1)
        while oPlayers[nPlayer2].round != nKeyAway:
            nPlayer2 = random.randint(0, len(oPlayers)-1)
            # print('{} {}'.format(nPlayer1, oPlayers[nPlayer1].round))
        oPlayers[nPlayer2].round = nKeyWin

        # Swap the players, so lowest ranking player in on the left.
        if oPlayers[nPlayer2].ranking < oPlayers[nPlayer1].ranking:
            nPlayer1, nPlayer2 = nPlayer2, nPlayer1

        # Play the match.
        oWinner, oLoser = PlayMatch(oPlayers[nPlayer1], oPlayers[nPlayer2], nScore)
        oLoser.round = nKeyLose



def PlaySeededTournament(oPlayers):
    ''' Play a tournament with seeded players. '''
    # Sort by pts.
    oPlayers = sorted(oPlayers, key=lambda CPlayer: CPlayer.pts, reverse=True)

    # Seed the players.
    nCount = 1
    for oPlayer in oPlayers:
        oPlayer.round = nCount
        if nCount < 9:
            nCount = nCount + 1
        # print('{:>5} {:<22}{:>4}'.format(nCount, oPlayer.NameWithRanking(), oPlayer.round), end='\n')


    # Qualifiying.
    print('Qualifying')
    PlayRound(oPlayers, 9, 9, 10, 0, 24, 5)

    # Round One.
    print('Round One')
    PlayRound(oPlayers, 1, 10, 12, -1, 1, 6)
    PlayRound(oPlayers, 10, 10, 12, -1, 1, 6)
    PlayRound(oPlayers, 10, 10, 13, -1, 1, 6)
    PlayRound(oPlayers, 8, 10, 13, -1, 1, 6)
    PlayRound(oPlayers, 5, 10, 14, -1, 1, 6)
    PlayRound(oPlayers, 10, 10, 14, -1, 1, 6)
    PlayRound(oPlayers, 10, 10, 15, -1, 1, 6)
    PlayRound(oPlayers, 4, 10, 15, -1, 1, 6)
    PlayRound(oPlayers, 3, 10, 16, -1, 1, 6)
    PlayRound(oPlayers, 10, 10, 16, -1, 1, 6)
    PlayRound(oPlayers, 10, 10, 17, -1, 1, 6)
    PlayRound(oPlayers, 6, 10, 17, -1, 1, 6)
    PlayRound(oPlayers, 7, 10, 18, -1, 1, 6)
    PlayRound(oPlayers, 10, 10, 18, -1, 1, 6)
    PlayRound(oPlayers, 10, 10, 19, -1, 1, 6)
    PlayRound(oPlayers, 2, 10, 19, -1, 1, 6)

    # Round Two.
    print('Round Two')
    PlayRound(oPlayers, 12, 12, 20, -2, 1, 9)
    PlayRound(oPlayers, 13, 13, 20, -2, 1, 9)
    PlayRound(oPlayers, 14, 14, 21, -2, 1, 9)
    PlayRound(oPlayers, 15, 15, 21, -2, 1, 9)
    PlayRound(oPlayers, 16, 16, 22, -2, 1, 9)
    PlayRound(oPlayers, 17, 17, 22, -2, 1, 9)
    PlayRound(oPlayers, 18, 18, 23, -2, 1, 9)
    PlayRound(oPlayers, 19, 19, 23, -2, 1, 9)

    # Quarter Finals.
    print('Quarter Finals')
    PlayRound(oPlayers, 20, 20, 30, -3, 1, 10)
    PlayRound(oPlayers, 21, 21, 30, -3, 1, 10)
    PlayRound(oPlayers, 22, 22, 31, -3, 1, 10)
    PlayRound(oPlayers, 23, 23, 31, -3, 1, 10)

    # Semi Finals.
    print('Semi Finals')
    PlayRound(oPlayers, 30, 30, 40, -4, 1, 13)
    PlayRound(oPlayers, 31, 31, 40, -4, 1, 13)

    print('Final')
    PlayRound(oPlayers, 40, 40, -6, -5, 1, 17)

    # Allocate ranking points and find the winner.
    oWinner = None
    for oPlayer in oPlayers:
        if oPlayer.round == 9:
            oPlayer.round = 0
        elif oPlayer.round == -6:
            oWinner = oPlayer
            oWinner.wins += 1
        elif oPlayer.round == -5:
            oPlayer.runner_up += 1

        nPts = [0, 1, 2, 4, 8, 16, 32][-oPlayer.round]
        oPlayer.history.append(nPts)
        while len(oPlayer.history) > 6:
            del oPlayer.history[0]
        oPlayer.pts = 0
        for nPts in oPlayer.history:
            oPlayer.pts += nPts

    # Return the winner.
    return oWinner



def PlayWorldChampionshipTournament(oPlayers):
    ''' Play a world championship tournament. '''
    # Sort by pts.
    oPlayers = sorted(oPlayers, key=lambda CPlayer: CPlayer.pts, reverse=True)

    # Seed the players.
    nCount = 1
    for oPlayer in oPlayers:
        oPlayer.round = nCount
        if nCount < 9:
            nCount = nCount + 1
        # print('{:>5} {:<22}{:>4}'.format(nCount, oPlayer.NameWithRanking(), oPlayer.round), end='\n')


    # Qualifiying.
    print('Qualifying')
    PlayRound(oPlayers, 9, 9, 10, 0, 24, 10)

    # Round One.
    print('Round One')
    PlayRound(oPlayers, 1, 10, 12, -1, 1, 10)
    PlayRound(oPlayers, 10, 10, 12, -1, 1, 10)
    PlayRound(oPlayers, 10, 10, 13, -1, 1, 10)
    PlayRound(oPlayers, 8, 10, 13, -1, 1, 10)
    PlayRound(oPlayers, 5, 10, 14, -1, 1, 10)
    PlayRound(oPlayers, 10, 10, 14, -1, 1, 10)
    PlayRound(oPlayers, 10, 10, 15, -1, 1, 10)
    PlayRound(oPlayers, 4, 10, 15, -1, 1, 10)
    PlayRound(oPlayers, 3, 10, 16, -1, 1, 10)
    PlayRound(oPlayers, 10, 10, 16, -1, 1, 10)
    PlayRound(oPlayers, 10, 10, 17, -1, 1, 10)
    PlayRound(oPlayers, 6, 10, 17, -1, 1, 10)
    PlayRound(oPlayers, 7, 10, 18, -1, 1, 10)
    PlayRound(oPlayers, 10, 10, 18, -1, 1, 10)
    PlayRound(oPlayers, 10, 10, 19, -1, 1, 10)
    PlayRound(oPlayers, 2, 10, 19, -1, 1, 10)

    # Round Two.
    print('Round Two')
    PlayRound(oPlayers, 12, 12, 20, -2, 1, 13)
    PlayRound(oPlayers, 13, 13, 20, -2, 1, 13)
    PlayRound(oPlayers, 14, 14, 21, -2, 1, 13)
    PlayRound(oPlayers, 15, 15, 21, -2, 1, 13)
    PlayRound(oPlayers, 16, 16, 22, -2, 1, 13)
    PlayRound(oPlayers, 17, 17, 22, -2, 1, 13)
    PlayRound(oPlayers, 18, 18, 23, -2, 1, 13)
    PlayRound(oPlayers, 19, 19, 23, -2, 1, 13)

    # Quarter Finals.
    print('Quarter Finals')
    PlayRound(oPlayers, 20, 20, 30, -3, 1, 13)
    PlayRound(oPlayers, 21, 21, 30, -3, 1, 13)
    PlayRound(oPlayers, 22, 22, 31, -3, 1, 13)
    PlayRound(oPlayers, 23, 23, 31, -3, 1, 13)

    # Semi Finals.
    print('Semi Finals')
    PlayRound(oPlayers, 30, 30, 40, -4, 1, 17)
    PlayRound(oPlayers, 31, 31, 40, -4, 1, 17)

    print('Final')
    PlayRound(oPlayers, 40, 40, -6, -5, 1, 18)

    # Allocate ranking points and find the winner.
    oWinner = None
    for oPlayer in oPlayers:
        if oPlayer.round == 9:
            oPlayer.round = 0
        elif oPlayer.round == -6:
            oWinner = oPlayer
            oWinner.wins += 1
        elif oPlayer.round == -5:
            oPlayer.runner_up += 1

        nPts = [0, 2, 4, 8, 16, 32, 64][-oPlayer.round]
        oPlayer.history.append(nPts)
        while len(oPlayer.history) > 6:
            del oPlayer.history[0]
        oPlayer.pts = 0
        for nPts in oPlayer.history:
            oPlayer.pts += nPts

    # Return the winner.
    return oWinner



def PlayOpenTournament(oPlayers):
    ''' Play a tournament with all the players. '''
    for oPlayer in oPlayers:
        oPlayer.round = 1

    # Qualifiying.
    print('Qualifying')
    PlayRound(oPlayers, 1, 1, 2, 0, 32, 5)

    # Round One.
    print('Round One')
    PlayRound(oPlayers, 2, 2, 3, -1, 16, 6)

    # Round Two.
    print('Round Two')
    PlayRound(oPlayers, 3, 3, 4, -2, 8, 6)

    # Quarter Finals.
    print('Quarter Finals')
    PlayRound(oPlayers, 4, 4, 5, -3, 4, 6)

    # Semi Finals.
    print('Semi Finals')
    PlayRound(oPlayers, 5, 5, 6, -4, 2, 9)

    print('Final')
    PlayRound(oPlayers, 6, 6, -6, -5, 1, 10)

    # Allocate ranking points and find the winner.
    oWinner = None
    for oPlayer in oPlayers:
        if oPlayer.round == -6:
            oWinner = oPlayer
            oWinner.wins += 1
        elif oPlayer.round == -5:
            oPlayer.runner_up += 1
        nPts = [0, 1, 2, 4, 8, 16, 32][-oPlayer.round]
        oPlayer.history.append(nPts)
        while len(oPlayer.history) > 6:
            del oPlayer.history[0]
        oPlayer.pts = 0
        for nPts in oPlayer.history:
            oPlayer.pts += nPts

    # Return the winner.
    return oWinner



def ShowRanking(oPlayers, bUpdate, nNumShow):
    ''' Display the players in ranking points order. '''
    # Sort by pts.
    oPlayers = sorted(oPlayers, key=lambda CPlayer: CPlayer.pts, reverse=True)
    # oPlayers = sorted(oPlayers, key=attrgetter('pts'), reverse=True)

    print('Top {}'.format(nNumShow))
    nCount = 1
    for oPlayer in oPlayers:
        if nCount <= nNumShow:
            if nCount == 1:
                oPlayer.top_ranking += 1
            print('{:>5} {:<22}{:>4}'.format(nCount, oPlayer.NameWithRanking(), oPlayer.pts), end='')
            for nPts in oPlayer.history:
                print('{:>3}'.format(nPts), end='')

            print('  ({})'.format(oPlayer.skill), end='')

            print()
        if bUpdate:
            oPlayer.ranking = nCount
        nCount = nCount + 1



def ShowWins(oPlayers):
    ''' Display the players in ranking points order. '''
    # Sort by pts.
    oPlayers = sorted(oPlayers, key=lambda CPlayer: (CPlayer.wins, CPlayer.runner_up), reverse=True)

    print('Wins ')
    nCount = 1
    for oPlayer in oPlayers:
        if oPlayer.wins > 0 or oPlayer.runner_up > 0:
            print('{:>5} {:<22}{:>4}{:>4}{:>8}'.format(nCount, oPlayer.NameWithRanking(), oPlayer.wins, oPlayer.runner_up, oPlayer.top_ranking), end='')

            print()
        nCount = nCount + 1



def Season(oPlayers, oSeasons):
    ''' Execute a season in the sport of life game. '''
    oWinner = PlayOpenTournament(oPlayers)
    ShowWins(oPlayers)
    ShowRanking(oPlayers, True, 16)
    sSeason = '{:<22}'.format(oWinner.name)
    for sHistory in oSeasons:
        print(sHistory)
    print('{}{}'.format(' ' * 22 * 5, sSeason))

    oWinner = PlaySeededTournament(oPlayers)
    ShowWins(oPlayers)
    ShowRanking(oPlayers, True, 16)
    sSeason = '{:<22}{}'.format(oWinner.name, sSeason)
    for sHistory in oSeasons:
        print(sHistory)
    print('{}{}'.format(' ' * 22 * 4, sSeason))

    oWinner = PlayOpenTournament(oPlayers)
    ShowWins(oPlayers)
    ShowRanking(oPlayers, True, 16)
    sSeason = '{:<22}{}'.format(oWinner.name, sSeason)
    for sHistory in oSeasons:
        print(sHistory)
    print('{}{}'.format(' ' * 22 * 3, sSeason))

    oWinner = PlaySeededTournament(oPlayers)
    ShowWins(oPlayers)
    ShowRanking(oPlayers, True, 16)
    sSeason = '{:<22}{}'.format(oWinner.name, sSeason)
    for sHistory in oSeasons:
        print(sHistory)
    print('{}{}'.format(' ' * 22 * 2, sSeason))

    oWinner = PlayOpenTournament(oPlayers)
    ShowWins(oPlayers)
    ShowRanking(oPlayers, True, 16)
    sSeason = '{:<22}{}'.format(oWinner.name, sSeason)
    for sHistory in oSeasons:
        print(sHistory)
    print('{}{}'.format(' ' * 22 * 1, sSeason))

    oWinner = PlayWorldChampionshipTournament(oPlayers)
    ShowWins(oPlayers)
    ShowRanking(oPlayers, True, 32)
    sSeason = '{:<22}{}'.format(oWinner.name, sSeason)
    for sHistory in oSeasons:
        print(sHistory)
    print(sSeason)

    # Returns the tournament winners this season.
    return sSeason



def Run():
    ''' Execute the sport of life game. '''

    # Create 32 players.
    oPlayers = []
    for nLoop in range(64):
        oPlayer = modPlayer.CPlayer(None)
        oPlayer.name = 'Player {}'.format(nLoop+1)
        oPlayer.skill = random.randint(100, 999)
        if nLoop <= 48:
            oPlayer.RandomName(0)
        else:
            oPlayer.RandomName(1)
        oPlayers.append(oPlayer)

    oSeasons = []
    for nLoop in range(5):
        sSeason = Season(oPlayers, oSeasons)
        oSeasons.append(sSeason)


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
