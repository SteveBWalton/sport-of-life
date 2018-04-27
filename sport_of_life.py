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
import modANSI



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



def PlaySeededTournament(oPlayers, sTitle, fPrizeMoney):
    '''
    Play a tournament with seeded players.
    64 Unseeded players in 2 qualifying rounds.
     '''
    print('{}{} (Seeded)'.format(' ' * 15, sTitle))

    # Sort by pts.
    oPlayers = sorted(oPlayers, key=lambda CPlayer: CPlayer.pts, reverse=True)

    # Seed the players.
    nCount = 1
    for oPlayer in oPlayers:
        oPlayer.round = nCount
        if nCount < 17:
            nCount = nCount + 1
        # print('{:>5} {:<22}{:>4}'.format(nCount, oPlayer.NameWithRanking(), oPlayer.round), end='\n')


    # Qualifiying.
    print('Qualifying 1')
    PlayRound(oPlayers, 17, 17, 18, 0, 32, 5)

    print('Qualifying 2')
    PlayRound(oPlayers, 18, 18, 19, 0, 16, 5)

    # Round One.
    print('Round One')
    PlayRound(oPlayers, 1, 19, 20, -1, 1, 6)
    PlayRound(oPlayers, 16, 19, 20, -1, 1, 6)
    PlayRound(oPlayers, 9, 19, 21, -1, 1, 6)
    PlayRound(oPlayers, 8, 19, 21, -1, 1, 6)
    PlayRound(oPlayers, 5, 19, 22, -1, 1, 6)
    PlayRound(oPlayers, 11, 19, 22, -1, 1, 6)
    PlayRound(oPlayers, 13, 19, 23, -1, 1, 6)
    PlayRound(oPlayers, 4, 19, 23, -1, 1, 6)
    PlayRound(oPlayers, 3, 19, 24, -1, 1, 6)
    PlayRound(oPlayers, 14, 19, 24, -1, 1, 6)
    PlayRound(oPlayers, 12, 19, 25, -1, 1, 6)
    PlayRound(oPlayers, 6, 19, 25, -1, 1, 6)
    PlayRound(oPlayers, 7, 19, 26, -1, 1, 6)
    PlayRound(oPlayers, 10, 19, 26, -1, 1, 6)
    PlayRound(oPlayers, 15, 19, 27, -1, 1, 6)
    PlayRound(oPlayers, 2, 19, 27, -1, 1, 6)

    # Round Two.
    print('Round Two')
    PlayRound(oPlayers, 20, 20, 30, -2, 1, 9)
    PlayRound(oPlayers, 21, 21, 30, -2, 1, 9)
    PlayRound(oPlayers, 22, 22, 31, -2, 1, 9)
    PlayRound(oPlayers, 23, 23, 31, -2, 1, 9)
    PlayRound(oPlayers, 24, 24, 32, -2, 1, 9)
    PlayRound(oPlayers, 25, 25, 32, -2, 1, 9)
    PlayRound(oPlayers, 26, 26, 33, -2, 1, 9)
    PlayRound(oPlayers, 27, 27, 33, -2, 1, 9)

    # Quarter Finals.
    print('Quarter Finals')
    PlayRound(oPlayers, 30, 30, 40, -3, 1, 10)
    PlayRound(oPlayers, 31, 31, 40, -3, 1, 10)
    PlayRound(oPlayers, 32, 32, 41, -3, 1, 10)
    PlayRound(oPlayers, 33, 33, 41, -3, 1, 10)

    # Semi Finals.
    print('Semi Finals')
    PlayRound(oPlayers, 40, 40, 50, -4, 1, 13)
    PlayRound(oPlayers, 41, 41, 50, -4, 1, 13)

    print('Final')
    PlayRound(oPlayers, 50, 50, -6, -5, 1, 17)

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
        while len(oPlayer.history) > 12:
            del oPlayer.history[0]
        oPlayer.pts = 0
        for nPts in oPlayer.history:
            oPlayer.pts += nPts

        # Prize Money.
        fMoney = fPrizeMoney * (nPts / 32)
        oPlayer.prize_money += fMoney
        oPlayer.season_money += fMoney


    # Wait.
    time.sleep(1)

    # Return the winner.
    return oWinner



def PlayWorldChampionshipTournament(oPlayers, fPrizeMoney):
    ''' Play a world championship tournament. '''
    print('{}World Championship'.format(' ' * 15))

    # Sort by pts.
    oPlayers = sorted(oPlayers, key=lambda CPlayer: CPlayer.pts, reverse=True)

    # Seed the players.
    nCount = 1
    for oPlayer in oPlayers:
        oPlayer.round = nCount
        if nCount < 17:
            nCount = nCount + 1
        # print('{:>5} {:<22}{:>4}'.format(nCount, oPlayer.NameWithRanking(), oPlayer.round), end='\n')

    # Qualifiying.
    print('Qualifying 1')
    PlayRound(oPlayers, 17, 17, 18, 0, 32, 10)

    print('Qualifying 2')
    PlayRound(oPlayers, 18, 18, 19, 0, 16, 10)

    # Round One.
    print('Round One')
    PlayRound(oPlayers, 1, 19, 20, -1, 1, 10)
    PlayRound(oPlayers, 16, 19, 20, -1, 1, 10)
    PlayRound(oPlayers, 9, 19, 21, -1, 1, 10)
    PlayRound(oPlayers, 8, 19, 21, -1, 1, 10)
    PlayRound(oPlayers, 5, 19, 22, -1, 1, 10)
    PlayRound(oPlayers, 11, 19, 22, -1, 1, 10)
    PlayRound(oPlayers, 13, 19, 23, -1, 1, 10)
    PlayRound(oPlayers, 4, 19, 23, -1, 1, 10)
    PlayRound(oPlayers, 3, 19, 24, -1, 1, 10)
    PlayRound(oPlayers, 14, 19, 24, -1, 1, 10)
    PlayRound(oPlayers, 12, 19, 25, -1, 1, 10)
    PlayRound(oPlayers, 6, 19, 25, -1, 1, 10)
    PlayRound(oPlayers, 7, 19, 26, -1, 1, 10)
    PlayRound(oPlayers, 10, 19, 26, -1, 1, 10)
    PlayRound(oPlayers, 15, 19, 27, -1, 1, 10)
    PlayRound(oPlayers, 2, 19, 27, -1, 1, 10)

    # Round Two.
    print('Round Two')
    PlayRound(oPlayers, 20, 20, 30, -2, 1, 13)
    PlayRound(oPlayers, 21, 21, 30, -2, 1, 13)
    PlayRound(oPlayers, 22, 22, 31, -2, 1, 13)
    PlayRound(oPlayers, 23, 23, 31, -2, 1, 13)
    PlayRound(oPlayers, 24, 24, 32, -2, 1, 13)
    PlayRound(oPlayers, 25, 25, 32, -2, 1, 13)
    PlayRound(oPlayers, 26, 26, 33, -2, 1, 13)
    PlayRound(oPlayers, 27, 27, 33, -2, 1, 13)

    # Quarter Finals.
    print('Quarter Finals')
    PlayRound(oPlayers, 30, 30, 40, -3, 1, 13)
    PlayRound(oPlayers, 31, 31, 40, -3, 1, 13)
    PlayRound(oPlayers, 32, 32, 41, -3, 1, 13)
    PlayRound(oPlayers, 33, 33, 41, -3, 1, 13)

    # Semi Finals.
    print('Semi Finals')
    PlayRound(oPlayers, 40, 40, 50, -4, 1, 17)
    PlayRound(oPlayers, 41, 41, 50, -4, 1, 17)

    print('Final')
    PlayRound(oPlayers, 50, 50, -6, -5, 1, 18)

    # Allocate ranking points and find the winner.
    oWinner = None
    for oPlayer in oPlayers:
        if oPlayer.round == 9:
            oPlayer.round = 0
        elif oPlayer.round == -6:
            oWinner = oPlayer
            oWinner.wins += 1
            oWinner.world_champion += 1
        elif oPlayer.round == -5:
            oPlayer.runner_up += 1

        nPts = [0, 2, 4, 8, 16, 32, 64][-oPlayer.round]
        oPlayer.history.append(nPts)

        while len(oPlayer.history) > 12:
            del oPlayer.history[0]
        oPlayer.pts = 0
        for nPts in oPlayer.history:
            oPlayer.pts += nPts

        # Prize Money.
        fMoney = fPrizeMoney * (nPts / 64)
        oPlayer.prize_money += fMoney
        oPlayer.season_money += fMoney

    # Wait.
    time.sleep(1)

    # Return the winner.
    return oWinner



def PlayOpenTournament(oPlayers, sTitle, fPrizeMoney):
    '''
    Play a tournament with all the players.
    Qualifying 1 80 Players 16 matches to get 64 players.
    Qualifying 2 64 players 32 matches to get 32 players.
    '''
    print('{}{} (Open)'.format(' ' * 15, sTitle))

    for oPlayer in oPlayers:
        oPlayer.round = 1

    # Qualifiying.
    print('Qualifying 1')
    PlayRound(oPlayers, 1, 1, 2, 0, 16, 5)

    # Put the winners back into qualifying.
    for oPlayer in oPlayers:
        if oPlayer.round == 2:
            oPlayer.round = 1

    print('Qualifying 2')
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
        while len(oPlayer.history) > 12:
            del oPlayer.history[0]
        oPlayer.pts = 0
        for nPts in oPlayer.history:
            oPlayer.pts += nPts

        # Prize Money.
        fMoney = fPrizeMoney * (nPts / 32)
        oPlayer.prize_money += fMoney
        oPlayer.season_money += fMoney

    # Wait.
    time.sleep(1)

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
            if oPlayer.age >= 40:
                sColour = modANSI.BOLD_CYAN
            elif oPlayer.age >= 35:
                sColour = modANSI.CYAN
            elif oPlayer.age <= 21:
                sColour = modANSI.YELLOW
            else:
                sColour = ''
            print('{:>5} {}{:<22}{}{:>4}'.format(nCount, sColour, oPlayer.NameWithRanking(), modANSI.RESET_ALL, oPlayer.pts), end='')
            print('{:>12,.2f}'.format(oPlayer.season_money), end='')
            for nPts in oPlayer.history:
                print('{:>3}'.format(nPts), end='')

            print('      ({})'.format(oPlayer.age), end='')
            print('      ({:>4})'.format(oPlayer.skill), end='')

            print()
        if bUpdate:
            oPlayer.ranking = nCount
        nCount = nCount + 1

    # Wait.
    time.sleep(1)


def UpdateSkill(oPlayers):
    ''' Update the skill of the players. '''
    for oPlayer in oPlayers:
        # Add age related skill.
        if oPlayer.age <= 20:
            oPlayer.skill += 10
        elif oPlayer.age <= 24:
            oPlayer.skill += 5
        elif oPlayer.age >= 40:
            oPlayer.skill -= 20
        elif oPlayer.age >= 35:
            oPlayer.skill -= 10
        elif oPlayer.age >= 30:
            oPlayer.skill -= 2

        # Add random skill.
        oPlayer.skill += random.randint(-10, 10)

        # Reset the short term shifts.
        if oPlayer.skill_offset != 0:
            if oPlayer.skill_offset > 0:
                oPlayer.skill += 100
                oPlayer.skill_offset -= 100
                print('{} is injuried ({}, {})'.format(oPlayer.NameWithRanking(), oPlayer.skill, oPlayer.skill_offset))
            else:
                oPlayer.skill -= 100
                oPlayer.skill_offset += 100
                print('{} is boosted ({}, {})'.format(oPlayer.NameWithRanking(), oPlayer.skill, oPlayer.skill_offset))


        if random.randint(0, 1000) == 0:
           print('{} has a boost.'.format(oPlayer.NameWithRanking()))
           oPlayer.skill += 500
           oPlayer.skill_offset -= 500
        if random.randint(0, 100) == 0:
            print('{} has an injury.'.format(oPlayer.NameWithRanking()))
            oPlayer.skill -= 500
            oPlayer.skill_offset += 500


        if oPlayer.skill < 100:
            oPlayer.skill = 100



def AddAge(oPlayers, oRetiredPlayers):
    ''' Update the age of the players. '''
    for oPlayer in oPlayers:
        oPlayer.age += 1
        if oPlayer.ranking > 70 and oPlayer.age > 35:
            print('{} has retired, aged {}. '.format(oPlayer.name, oPlayer.age), end='')
            oRetiredPlayer = oPlayer.Retire()
            oRetiredPlayers.append(oRetiredPlayer)

            oPlayer.Reset()
            oPlayer.skill = oPlayer.skill = random.randint(100, 899)
            nCulture = 0
            if random.randint(0, 6) == 4:
                nCulture = 1
            oPlayer.RandomName(nCulture)
            print('{} has joined the tour.'.format(oPlayer.name))

    # Wait.
    time.sleep(1)

    # Return the new list of retired players
    return oRetiredPlayers



def ShowWins(oPlayers, oRetiredPlayers):
    ''' Display the players in ranking points order. '''
    # Sort by pts.
    oPlayers = sorted(oPlayers + oRetiredPlayers, key=lambda CPlayer: (CPlayer.wins, CPlayer.runner_up), reverse=True)

    print('Wins ')
    nCount = 1
    for oPlayer in oPlayers:
        if oPlayer.wins > 0 or oPlayer.runner_up > 0:
            if oPlayer.ranking > 500:
                print('{:>5} {}{:<28}{}{:>4}{:>4}{:>8}{:>8.1f}{:>14,.2f}'.format(nCount, modANSI.CYAN, oPlayer.NameWithYearRange(), modANSI.RESET_ALL, oPlayer.wins, oPlayer.runner_up, oPlayer.world_champion, oPlayer.top_ranking / 6, oPlayer.prize_money), end='')

            else:
                print('{:>5} {:<28}{:>4}{:>4}{:>8}{:>8.1f}{:>14,.2f}'.format(nCount, oPlayer.NameWithRanking(), oPlayer.wins, oPlayer.runner_up, oPlayer.world_champion, oPlayer.top_ranking / 6, oPlayer.prize_money), end='')

            print()
        nCount = nCount + 1

    # Wait.
    time.sleep(1)



def ShowChampions(oSeasons, nThisSeason, sThisSeason, nIndex):
    ''' Display the previous champions. '''
    # print('1234 123456789012345678901212345678901234567890121234567890123456789012123456789012345678901212345678901234567890121234567890123456789012')
    print('{}'.format(modANSI.MAGENTA), end='')
    print('     World                 China                 German                UK                    Welsh                 Shanghai')
    print('     Champion              Open                  Masters               Championship          Open                  Masters{}'.format(modANSI.RESET_ALL))
    for sHistory in oSeasons:
        print(sHistory)
    if sThisSeason != '':
        print('{} {}{}'.format(nThisSeason, ' ' * (22 * nIndex), sThisSeason))



def Season(oPlayers, oSeasons, oRetiredPlayers, nSeason, fPrizeMoney):
    ''' Execute a season in the sport of life game. '''
    # Reset for the season.
    for oPlayer in oPlayers:
        oPlayer.season_money = 0

    # Play the season.
    oWinner = PlayOpenTournament(oPlayers, 'Shanghai Masters', 0.3 * fPrizeMoney)
    ShowWins(oPlayers, oRetiredPlayers)
    ShowRanking(oPlayers, True, 16)
    sSeason = '{:<22}'.format(oWinner.name)
    ShowChampions(oSeasons, nSeason, sSeason, 5)
    oWinner.first_win = oWinner.first_win if oWinner.first_win != None else nSeason
    oWinner.last_win = nSeason
    UpdateSkill(oPlayers)

    oWinner = PlayOpenTournament(oPlayers, 'Welsh Open', 0.3 * fPrizeMoney)
    ShowWins(oPlayers, oRetiredPlayers)
    ShowRanking(oPlayers, True, 16)
    sSeason = '{:<22}{}'.format(oWinner.name, sSeason)
    ShowChampions(oSeasons, nSeason, sSeason, 4)
    oWinner.first_win = oWinner.first_win if oWinner.first_win != None else nSeason
    oWinner.last_win = nSeason
    UpdateSkill(oPlayers)

    oWinner = PlaySeededTournament(oPlayers, 'UK Championship', 0.6 * fPrizeMoney)
    ShowWins(oPlayers, oRetiredPlayers)
    ShowRanking(oPlayers, True, 16)
    sSeason = '{:<22}{}'.format(oWinner.name, sSeason)
    ShowChampions(oSeasons, nSeason, sSeason, 3)
    oWinner.first_win = oWinner.first_win if oWinner.first_win != None else nSeason
    oWinner.last_win = nSeason
    UpdateSkill(oPlayers)

    oWinner = PlayOpenTournament(oPlayers, 'German Masters', 0.3 * fPrizeMoney)
    ShowWins(oPlayers, oRetiredPlayers)
    ShowRanking(oPlayers, True, 16)
    sSeason = '{:<22}{}'.format(oWinner.name, sSeason)
    ShowChampions(oSeasons, nSeason, sSeason, 2)
    oWinner.first_win = oWinner.first_win if oWinner.first_win != None else nSeason
    oWinner.last_win = nSeason
    UpdateSkill(oPlayers)

    oWinner = PlaySeededTournament(oPlayers, 'China Open', 0.6 * fPrizeMoney)
    ShowWins(oPlayers, oRetiredPlayers)
    ShowRanking(oPlayers, True, 16)
    sSeason = '{:<22}{}'.format(oWinner.name, sSeason)
    ShowChampions(oSeasons, nSeason, sSeason, 1)
    oWinner.first_win = oWinner.first_win if oWinner.first_win != None else nSeason
    oWinner.last_win = nSeason
    UpdateSkill(oPlayers)

    oWinner = PlayWorldChampionshipTournament(oPlayers, fPrizeMoney)
    ShowWins(oPlayers, oRetiredPlayers)
    ShowRanking(oPlayers, True, 80)
    time.sleep(10)
    sSeason = '{:<22}{}'.format(oWinner.name, sSeason)
    ShowChampions(oSeasons, nSeason, sSeason, 0)
    oWinner.first_win = oWinner.first_win if oWinner.first_win != None else nSeason
    oWinner.last_win = nSeason
    UpdateSkill(oPlayers)

    # Age and retire the players.
    oRetiredPlayers = AddAge(oPlayers, oRetiredPlayers)

    # Wait.
    time.sleep(10)

    # Returns the tournament winners this season.
    return sSeason, oRetiredPlayers



def Run():
    ''' Execute the sport of life game. '''

    # Create 80 players.
    print('80 players join the tour. ', end='')
    oPlayers = []
    for nLoop in range(80):
        oPlayer = modPlayer.CPlayer(None)
        oPlayer.skill = random.randint(100, 999)
        oPlayer.age = random.randint(20, 36)
        if nLoop < 100:
            oPlayer.RandomName(0)
        else:
            oPlayer.RandomName(1)
        oPlayers.append(oPlayer)
    print()

    nPlayerID = random.randint(0, len(oPlayers)-1)
    oPlayer = oPlayers[nPlayerID]
    print('{} has an injury.'.format(oPlayer.name))
    oPlayer.skill -= 600
    oPlayer.skill_offset += 600
    if oPlayer.skill < 100:
        oPlayer.skill = 100
    print('{} {} {}'.format(oPlayer.name, oPlayer.skill, oPlayer.skill_offset))

    oRetiredPlayers = []
    oSeasons = []
    nLoop = 1970
    fPrizeMoney = 200000.0
    while nLoop > 1:
        sSeason, oRetiredPlayers = Season(oPlayers, oSeasons, oRetiredPlayers, nLoop, fPrizeMoney)

        # Find the season end number 1 player.
        oNumberOne = None
        oTopMoney = oPlayers[0]
        for oPlayer in oPlayers:
            if oPlayer.ranking == 1:
                oNumberOne = oPlayer
            if oPlayer.season_money > oTopMoney.season_money:
                oTopMoney = oPlayer

        oSeasons.append('{} {} {:>4} {:<22} {:>12,.2f} {}'.format(nLoop, sSeason, oNumberOne.pts, oNumberOne.name, oTopMoney.season_money, oTopMoney.name))

        fPrizeMoney *= 1.05
        nLoop += 1

        # Wait.
        time.sleep(1)



if __name__ == '__main__':
    # Process the command line arguments.
    # This might end the program (--help).
    oParse = argparse.ArgumentParser(prog='sport_of_life', description='Little game to run under Linux and Windows.')
    oArgs = oParse.parse_args()

    # Welcome message.
    print('{}Sport Of Life{} by Steve Walton.'.format(modANSI.RED, modANSI.RESET_ALL))
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
