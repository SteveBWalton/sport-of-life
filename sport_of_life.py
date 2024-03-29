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
import time
import random

# Application Libraries.
from player import Player
from inkey import InKey
import ansi



class Game:
    ''' Class to represent the game.'''



    def __init__(self):
        ''' Class constructor. '''
        self.isWait = True
        self.isFullRanking = False
        self.isExitGame = False
        self.highlight = ''
        self.avgSkill = 0.0



    def playMatch(self, player1, player2, winTarget):
        ''' Play a match between the specified players. '''
        score1 = 0
        score2 = 0
        while score1 < winTarget and score2 < winTarget:
            if random.randrange(player1.skill) >= random.randrange(player2.skill):
                score1 += 1
            else:
                score2 += 1
            player1Colour = ansi.MAGENTA if self.highlight == player1.name else ''
            player2Colour = ansi.MAGENTA if self.highlight == player2.name else ''
            resetScore = ansi.RESET_ALL

            # Highlight a close score.
            if score1 >= winTarget - 1  and score2 >= winTarget - 1:
                resetScore = ansi.RED
                if player2Colour == '':
                    player2Colour = ansi.RESET_ALL

            print(f'{player1Colour}{player1.nameWithRanking():>22}{resetScore} {score1:>2} - {score2:<2} {player2Colour}{player2.nameWithRanking():<22}{ansi.RESET_ALL}', end='\r', flush=True)

            self.processKeys(player1, player2)

            if self.isWait:
                # Wait.
                time.sleep(0.25)
                # Extra wait before
                if score1 == winTarget - 1  and score2 == winTarget - 1:
                    time.sleep(1.0)

        print()

        # Return the winner and loser.
        if score1 > score2:
            return player1, player2
        return player2, player1



    def playRound(self, players, keyHome, keyAway, keyWin, keyLose, numMatches, scoreTarget):
        ''' Play a round of a tournament. '''
        for _matchCount in range(numMatches):
            # Find 2 players that are in this round.
            player1Index = random.randint(0, len(players)-1)
            while players[player1Index].round != keyHome:
                player1Index = random.randint(0, len(players)-1)
            players[player1Index].round = keyWin

            player2Index = random.randint(0, len(players)-1)
            while players[player2Index].round != keyAway:
                player2Index = random.randint(0, len(players)-1)
            players[player2Index].round = keyWin

            # Swap the players, so lowest ranking player in on the left.
            if players[player2Index].ranking < players[player1Index].ranking:
                player1Index, player2Index = player2Index, player1Index

            # Play the match.
            _winner, loser = self.playMatch(players[player1Index], players[player2Index], scoreTarget)
            loser.round = keyLose



    def playSeededTournament(self, players, title, prizeMoney):
        '''
        Play a tournament with seeded players.
        64 Unseeded players in 2 qualifying rounds.
         '''
        print(f'{" " * 15}{title} (Seeded)')
        self.isWait = True

        # Sort by pts.
        players = sorted(players, key=lambda Player: Player.pts, reverse=True)

        # Seed the players.
        count = 1
        for player in players:
            player.round = count
            if count < 17:
                count += 1
            # print('{:>5} {:<22}{:>4}'.format(count, player.nameWithRanking(), player.round), end='\n')


        # Qualifiying.
        print(f'{title} Qualifying 1')
        self.playRound(players, 17, 17, 18, 0, 32, 5)

        print(f'{title} Qualifying 2')
        self.playRound(players, 18, 18, 19, 0, 16, 5)

        # Round One.
        print(f'{title} Round One')
        self.playRound(players, 1, 19, 20, -1, 1, 6)
        self.playRound(players, 16, 19, 20, -1, 1, 6)
        self.playRound(players, 9, 19, 21, -1, 1, 6)
        self.playRound(players, 8, 19, 21, -1, 1, 6)
        self.playRound(players, 5, 19, 22, -1, 1, 6)
        self.playRound(players, 11, 19, 22, -1, 1, 6)
        self.playRound(players, 13, 19, 23, -1, 1, 6)
        self.playRound(players, 4, 19, 23, -1, 1, 6)
        self.playRound(players, 3, 19, 24, -1, 1, 6)
        self.playRound(players, 14, 19, 24, -1, 1, 6)
        self.playRound(players, 12, 19, 25, -1, 1, 6)
        self.playRound(players, 6, 19, 25, -1, 1, 6)
        self.playRound(players, 7, 19, 26, -1, 1, 6)
        self.playRound(players, 10, 19, 26, -1, 1, 6)
        self.playRound(players, 15, 19, 27, -1, 1, 6)
        self.playRound(players, 2, 19, 27, -1, 1, 6)

        # Round Two.
        print(f'{title} Round Two')
        self.playRound(players, 20, 20, 30, -2, 1, 9)
        self.playRound(players, 21, 21, 30, -2, 1, 9)
        self.playRound(players, 22, 22, 31, -2, 1, 9)
        self.playRound(players, 23, 23, 31, -2, 1, 9)
        self.playRound(players, 24, 24, 32, -2, 1, 9)
        self.playRound(players, 25, 25, 32, -2, 1, 9)
        self.playRound(players, 26, 26, 33, -2, 1, 9)
        self.playRound(players, 27, 27, 33, -2, 1, 9)

        # Quarter Finals.
        print(f'{title} Quarter Finals')
        self.playRound(players, 30, 30, 40, -3, 1, 10)
        self.playRound(players, 31, 31, 40, -3, 1, 10)
        self.playRound(players, 32, 32, 41, -3, 1, 10)
        self.playRound(players, 33, 33, 41, -3, 1, 10)

        # Semi Finals.
        print(f'{title} Semi Finals')
        self.playRound(players, 40, 40, 50, -4, 1, 13)
        self.playRound(players, 41, 41, 50, -4, 1, 13)

        print(f'{title} Final')
        self.playRound(players, 50, 50, -6, -5, 1, 17)

        # Allocate ranking points and find the winner.
        winner = None
        for player in players:
            if player.round == 9:
                player.round = 0
            elif player.round == -6:
                winner = player
                winner.wins += 1
            elif player.round == -5:
                player.runnerUp += 1

            pts = [0, 1, 2, 4, 8, 16, 32][-player.round]
            player.history.append(pts)
            while len(player.history) > 12:
                del player.history[0]
            player.pts = 0
            for pts in player.history:
                player.pts += pts

            # Prize Money.
            moneyIndex = [0, 13, 28, 42, 56, 75, 100][-player.round]
            actualMoney = prizeMoney * (moneyIndex / 100)
            player.prizeMoney += actualMoney
            player.seasonMoney += actualMoney

        # Wait.
        time.sleep(1)

        # Return the winner.
        return winner



    def playWorldChampionshipTournament(self, players, prizeMoney):
        ''' Play a world championship tournament. '''
        print(f'{" " * 15}World Championship')
        self.isWait = True

        # Sort by pts.
        players = sorted(players, key=lambda Player: Player.pts, reverse=True)

        # Seed the players.
        count = 1
        for player in players:
            player.round = count
            if count < 17:
                count += 1
            # print('{:>5} {:<22}{:>4}'.format(count, player.nameWithRanking(), player.round), end='\n')

        # Qualifiying.
        print('World Championship Qualifying 1')
        self.playRound(players, 17, 17, 18, 0, 32, 10)

        print('World Championship Qualifying 2')
        self.playRound(players, 18, 18, 19, 0, 16, 10)

        # Round One.
        print('World Championship Round One')
        self.playRound(players, 1, 19, 20, -1, 1, 10)
        self.playRound(players, 16, 19, 20, -1, 1, 10)
        self.playRound(players, 9, 19, 21, -1, 1, 10)
        self.playRound(players, 8, 19, 21, -1, 1, 10)
        self.playRound(players, 5, 19, 22, -1, 1, 10)
        self.playRound(players, 11, 19, 22, -1, 1, 10)
        self.playRound(players, 13, 19, 23, -1, 1, 10)
        self.playRound(players, 4, 19, 23, -1, 1, 10)
        self.playRound(players, 3, 19, 24, -1, 1, 10)
        self.playRound(players, 14, 19, 24, -1, 1, 10)
        self.playRound(players, 12, 19, 25, -1, 1, 10)
        self.playRound(players, 6, 19, 25, -1, 1, 10)
        self.playRound(players, 7, 19, 26, -1, 1, 10)
        self.playRound(players, 10, 19, 26, -1, 1, 10)
        self.playRound(players, 15, 19, 27, -1, 1, 10)
        self.playRound(players, 2, 19, 27, -1, 1, 10)

        # Round Two.
        print('World Championship Round Two')
        self.playRound(players, 20, 20, 30, -2, 1, 13)
        self.playRound(players, 21, 21, 30, -2, 1, 13)
        self.playRound(players, 22, 22, 31, -2, 1, 13)
        self.playRound(players, 23, 23, 31, -2, 1, 13)
        self.playRound(players, 24, 24, 32, -2, 1, 13)
        self.playRound(players, 25, 25, 32, -2, 1, 13)
        self.playRound(players, 26, 26, 33, -2, 1, 13)
        self.playRound(players, 27, 27, 33, -2, 1, 13)

        # Quarter Finals.
        print('World Championship Quarter Finals')
        self.playRound(players, 30, 30, 40, -3, 1, 13)
        self.playRound(players, 31, 31, 40, -3, 1, 13)
        self.playRound(players, 32, 32, 41, -3, 1, 13)
        self.playRound(players, 33, 33, 41, -3, 1, 13)

        # Semi Finals.
        print('World Championship Semi Finals')
        self.playRound(players, 40, 40, 50, -4, 1, 17)
        self.playRound(players, 41, 41, 50, -4, 1, 17)

        print('World Championship Final')
        self.playRound(players, 50, 50, -6, -5, 1, 18)

        # Allocate ranking points and find the winner.
        winner = None
        for player in players:
            if player.round == 9:
                player.round = 0
            elif player.round == -6:
                winner = player
                winner.wins += 1
                winner.worldChampion += 1
            elif player.round == -5:
                player.runnerUp += 1

            pts = [0, 2, 4, 8, 16, 32, 64][-player.round]
            player.history.append(pts)

            while len(player.history) > 12:
                del player.history[0]
            player.pts = 0
            for pts in player.history:
                player.pts += pts

            # Prize Money.
            moneyIndex = [0, 13, 28, 42, 56, 75, 100][-player.round]
            actualMoney = prizeMoney * (moneyIndex / 100)
            player.prizeMoney += actualMoney
            player.seasonMoney += actualMoney

        # Wait.
        time.sleep(1)

        # Return the winner.
        return winner



    def playOpenTournament(self, players, title, prizeMoney):
        '''
        Play a tournament with all the players.
        Qualifying 1 80 Players 16 matches to get 64 players.
        Qualifying 2 64 players 32 matches to get 32 players.
        '''
        print(f'{" " * 15}{title} (Open)')
        self.isWait = True

        for player in players:
            player.round = 1

        # Qualifiying.
        print(f'{title} Qualifying 1')
        self.playRound(players, 1, 1, 2, 0, 16, 5)

        # Put the winners back into qualifying.
        for player in players:
            if player.round == 2:
                player.round = 1

        print(f'{title} Qualifying 2')
        self.playRound(players, 1, 1, 2, 0, 32, 5)

        # Round One.
        print(f'{title} Round One')
        self.playRound(players, 2, 2, 3, -1, 16, 6)

        # Round Two.
        print(f'{title} Round Two')
        self.playRound(players, 3, 3, 4, -2, 8, 6)

        # Quarter Finals.
        print(f'{title} Quarter Finals')
        self.playRound(players, 4, 4, 5, -3, 4, 6)

        # Semi Finals.
        print(f'{title} Semi Finals')
        self.playRound(players, 5, 5, 6, -4, 2, 9)

        print(f'{title} Final')
        self.playRound(players, 6, 6, -6, -5, 1, 10)

        # Allocate ranking points and find the winner.
        winner = None
        for player in players:
            if player.round == -6:
                winner = player
                winner.wins += 1
            elif player.round == -5:
                player.runnerUp += 1
            pts = [0, 1, 2, 4, 8, 16, 32][-player.round]
            player.history.append(pts)
            while len(player.history) > 12:
                del player.history[0]
            player.pts = 0
            for pts in player.history:
                player.pts += pts

            # Prize Money.
            moneyIndex = [0, 13, 28, 42, 56, 75, 100][-player.round]
            actualMoney = prizeMoney * (moneyIndex / 100)
            player.prizeMoney += actualMoney
            player.seasonMoney += actualMoney

        # Wait.
        time.sleep(1)

        # Return the winner.
        return winner



    def showRanking(self, players, isUpdate, numShow):  # pylint: disable=no-self-use
        ''' Display the players in ranking points order. '''
        # Sort by pts.
        players = sorted(players, key=lambda Player: Player.pts, reverse=True)
        # players = sorted(players, key=attrgetter('pts'), reverse=True)

        print(f'Top {numShow}')
        count = 1
        for player in players:
            if count <= numShow:
                if count == 1:
                    player.topRanking += 1
                if self.highlight == player.name:
                    colour = ansi.MAGENTA
                elif player.age >= 40:
                    colour = ansi.BOLD_CYAN
                elif player.age >= 35:
                    colour = ansi.CYAN
                elif player.age <= 21:
                    colour = ansi.YELLOW
                else:
                    colour = ''
                if player.round == -6:
                    # Winner of last tournament.
                    colour = ansi.RED
                print(f'{count:>5} {colour}{player.nameWithRanking():<22}{player.pts:>4}', end='')
                print(f'{player.seasonMoney:>13,.2f}', end='')
                for pts in player.history:
                    print(f'{pts:>3}', end='')

                print(f'      ({player.age})', end='')
                print(f'      ({player.skill:>4})', end='')

                print(f'{ansi.RESET_ALL}')
            if isUpdate:
                player.ranking = count
            count += 1

        # Wait.
        time.sleep(1)


    # pylint: disable=no-self-use
    def updateSkill(self, players):
        ''' Update the skill of the players. '''
        avgSkill = 0.0
        for player in players:
            # Add age related skill.
            if player.age <= 20:
                player.skill += 10
            elif player.age <= 24:
                player.skill += 5
            elif player.age >= 40:
                player.skill -= 20
            elif player.age >= 35:
                player.skill -= 10
            elif player.age >= 30:
                player.skill -= 2

            # Add bias.
            if self.highlight == player.name:
                player.skill += 3

            # Add random skill.
            player.skill += random.randint(-20, 20)

            # Reset the short term shifts.
            if player.skillOffset != 0:
                if player.skillOffset > 0:
                    player.skill += 100
                    player.skillOffset -= 100
                    print(f'{player.nameWithRanking()} is injuried ({player.skill}, {player.skillOffset})')
                else:
                    player.skill -= 100
                    player.skillOffset += 100
                    print(f'{player.nameWithRanking()} is boosted ({player.skill}, {player.skillOffset})')

            # Add some random short term shifts.
            if random.randint(0, 1000) == 0:
                print(f'{player.nameWithRanking()} has a boost.')
                player.skill += 600
                player.skillOffset -= 600
            if random.randint(0, 100) == 0:
                print(f'{player.nameWithRanking()} has an injury.')
                player.skill -= 500
                player.skillOffset += 500

            # Soft skill upper limit.
            if player.skill > 999:
                player.skill -= 1

            # Hard skill lower limit.
            player.skill = max(100, player.skill)

            avgSkill += player.skill / len(players)

        print(f'Average Skill = {avgSkill:.1f} <= {self.avgSkill:.1f}')
        self.avgSkill = avgSkill



    def addAge(self, players, retiredPlayers):  # pylint: disable=no-self-use
        ''' Update the age of the players. '''
        for player in players:
            player.age += 1
            if player.ranking > 70 and player.age > 35:
                print(f'{player.name} has retired, aged {player.age}. ', end='')
                retiredPlayer = player.retire()
                retiredPlayers.append(retiredPlayer)

                player.reset()
                player.skill = random.randint(50, 450) + random.randint(50, 450)
                cultureIndex = 0
                if random.randint(0, 6) == 4:
                    cultureIndex = 1
                player.randomName(cultureIndex)
                print(f'{player.name} has joined the tour.')

        # Wait.
        time.sleep(1)

        # Return the new list of retired players
        return retiredPlayers



    def showWins(self, players, retiredPlayers):    # pylint: disable=no-self-use
        ''' Display the players in ranking points order. '''
        # Sort by pts.
        players = sorted(players + retiredPlayers, key=lambda Player: (Player.wins, Player.runnerUp), reverse=True)

        print('Wins ')
        count = 1
        for player in players:
            if player.wins > 0 or player.runnerUp > 0:
                if player.ranking > 500:
                    print(f'{count:>5} {ansi.CYAN}{player.nameWithYearRange():<28}{player.wins:>4}{player.wins + player.runnerUp:>4}{player.worldChampion:>8}{player.topRanking / 6:>8.1f}{player.prizeMoney:>14,.2f}{ansi.RESET_ALL}', end='')

                else:
                    if player.round == -6:
                        # Winner of last tournament.
                        print(f'{count:>5} {ansi.RED}{player.nameWithRanking():<28}{player.wins:>4}{player.wins + player.runnerUp:>4}{player.worldChampion:>8}{player.topRanking / 6:>8.1f}{player.prizeMoney:>14,.2f}{ansi.RESET_ALL}', end='')
                    else:
                        print(f'{count:>5} {player.nameWithRanking():<28}{player.wins:>4}{player.wins + player.runnerUp:>4}{player.worldChampion:>8}{player.topRanking / 6:>8.1f}{player.prizeMoney:>14,.2f}', end='')

                print()
            count += 1

        # Wait.
        time.sleep(1)



    def showChampions(self, seasons, seasonYear, seasonDescription, indent):    #pylint: disable=no-self-use
        ''' Display the previous champions. '''
        print(f'{ansi.MAGENTA}', end='')
        print('     World                 China                 German                UK                    Welsh                 Shanghai')
        print(f'     Champion              Open                  Masters               Championship          Open                  Masters{ansi.RESET_ALL}')
        for history in seasons:
            print(history)
        if seasonDescription != '':
            print(f'{seasonYear} {" " * (22 * indent)}{seasonDescription}')



    def playSeason(self, players, seasons, retiredPlayers, seasonIndex, prizeMoney):
        ''' Execute a season in the sport of life game. '''
        # reset for the season.
        for player in players:
            player.seasonMoney = 0

        # Play the season.
        if not self.isExitGame:
            winner = self.playOpenTournament(players, 'Shanghai Masters', 0.3 * prizeMoney)
            self.showWins(players, retiredPlayers)
            if self.isFullRanking:
                self.showRanking(players, True, 80)
                self.isFullRanking = False
            else:
                self.showRanking(players, True, 17)
            seasonDescription = f'{winner.name:<22}'
            self.showChampions(seasons, seasonIndex, seasonDescription, 5)
            winner.firstWin = winner.firstWin if winner.firstWin is not None else seasonIndex
            winner.lastWin = seasonIndex
            self.updateSkill(players)

        if not self.isExitGame:
            winner = self.playOpenTournament(players, 'Welsh Open', 0.3 * prizeMoney)
            self.showWins(players, retiredPlayers)
            if self.isFullRanking:
                self.showRanking(players, True, 80)
                self.isFullRanking = False
            else:
                self.showRanking(players, True, 17)
            seasonDescription = f'{winner.name:<22}{seasonDescription}'
            self.showChampions(seasons, seasonIndex, seasonDescription, 4)
            winner.firstWin = winner.firstWin if winner.firstWin is not None else seasonIndex
            winner.lastWin = seasonIndex
            self.updateSkill(players)

        if not self.isExitGame:
            winner = self.playSeededTournament(players, 'UK Championship', 0.6 * prizeMoney)
            self.showWins(players, retiredPlayers)
            if self.isFullRanking:
                self.showRanking(players, True, 80)
                self.isFullRanking = False
            else:
                self.showRanking(players, True, 17)
            seasonDescription = f'{winner.name:<22}{seasonDescription}'
            self.showChampions(seasons, seasonIndex, seasonDescription, 3)
            winner.firstWin = winner.firstWin if winner.firstWin is not None else seasonIndex
            winner.lastWin = seasonIndex
            self.updateSkill(players)

        if not self.isExitGame:
            winner = self.playOpenTournament(players, 'German Masters', 0.3 * prizeMoney)
            self.showWins(players, retiredPlayers)
            if self.isFullRanking:
                self.showRanking(players, True, 80)
                self.isFullRanking = False
            else:
                self.showRanking(players, True, 17)
            seasonDescription = f'{winner.name:<22}{seasonDescription}'
            self.showChampions(seasons, seasonIndex, seasonDescription, 2)
            winner.firstWin = winner.firstWin if winner.firstWin is not None else seasonIndex
            winner.lastWin = seasonIndex
            self.updateSkill(players)

        if not self.isExitGame:
            winner = self.playSeededTournament(players, 'China Open', 0.6 * prizeMoney)
            self.showWins(players, retiredPlayers)
            if self.isFullRanking:
                self.showRanking(players, True, 80)
                self.isFullRanking = False
            else:
                self.showRanking(players, True, 17)
            seasonDescription = f'{winner.name:<22}{seasonDescription}'
            self.showChampions(seasons, seasonIndex, seasonDescription, 1)
            winner.firstWin = winner.firstWin if winner.firstWin is not None else seasonIndex
            winner.lastWin = seasonIndex
            self.updateSkill(players)

        if not self.isExitGame:
            winner = self.playWorldChampionshipTournament(players, prizeMoney)
            self.showWins(players, retiredPlayers)
            self.showRanking(players, True, 80)
            time.sleep(10)
            seasonDescription = f'{winner.name:<22}{seasonDescription}'
            self.showChampions(seasons, seasonIndex, seasonDescription, 0)
            winner.firstWin = winner.firstWin if winner.firstWin is not None else seasonIndex
            winner.lastWin = seasonIndex
            self.updateSkill(players)

        # Age and retire the players.
        if not self.isExitGame:
            retiredPlayers = self.addAge(players, retiredPlayers)

        # Wait.
        if not self.isExitGame:
            time.sleep(10)

        # Returns the tournament winners this season.
        return seasonDescription, retiredPlayers



    def selectHighlight(self, player1, player2):
        ''' Select the highlighted player. '''
        print()
        print('Select Highlight')
        print(f'1) {player1.name}')
        print(f'2) {player2.name}')
        print('3) Remove highlight')
        print(f'4) Keep {self.highlight}')
        keyScan = self.keyboard.scanKey()
        # while keyScan != '1' and keyScan != '2' and keyScan != '3' and keyScan != '4':
        while keyScan not in ('1', '2', '3', '4'):
            keyScan = self.keyboard.scanKey()

        if keyScan == '1':
            self.highlight = player1.name
        if keyScan == '2':
            self.highlight = player2.name
        if keyScan == '3':
            self.highlight = ''



    def processKeys(self, player1, player2):
        ''' Scan the keyboard for a key and deal with any key presses. '''
        keyScan = self.keyboard.scanKey()
        if keyScan == 'q':
            self.isExitGame = True
            self.isWait = False
        if keyScan == ' ':
            self.isWait = False
        if keyScan == 'r':
            self.isFullRanking = True
        if keyScan == 'h':
            self.selectHighlight(player1, player2)



    def showKeys(self): # pylint: disable=no-self-use
        ''' Display the keys that are used in the program. '''
        print('Keys')
        print('   q    Quit the program.')
        print('[space] Complete the tournament.')
        print('   r    Show full ranking table at the end of tournament.')
        print('   h    Select player to highlight.')



    def run(self):
        ''' Execute the sport of life game. '''
        # Create a keyboard scan.
        self.keyboard = InKey()
        self.isExitGame = False

        # Create 80 players.
        print('80 players join the tour. ', end='')
        players = []
        self.avgSkill = 0
        for loop in range(80):
            player = Player(None)
            player.skill = random.randint(100, 999)
            player.age = random.randint(20, 36)
            if loop < 100:
                player.randomName(0)
            else:
                player.randomName(1)
            players.append(player)
            self.avgSkill += player.skill / 80.0
        print()


        playerIndex = random.randint(0, len(players)-1)
        player = players[playerIndex]
        print(f'{player.name} has an injury.')
        player.skill -= 600
        player.skillOffset += 600
        player.skill = max(100, player.skill)
        print(f'{player.name} {player.skill} {player.skillOffset}')

        retiredPlayers = []
        seasons = []
        loop = 1968
        prizeMoney = 200000.0
        while not self.isExitGame:
            self.showKeys()
            seasonDescription, retiredPlayers = self.playSeason(players, seasons, retiredPlayers, loop, prizeMoney)

            # Find the season end number 1 player.
            numberOnePlayer = None
            topMoneyPlayer = players[0]
            for player in players:
                if player.ranking == 1:
                    numberOnePlayer = player
                if player.seasonMoney > topMoneyPlayer.seasonMoney:
                    topMoneyPlayer = player

            seasons.append(f'{loop} {seasonDescription} {numberOnePlayer.pts:>4} {numberOnePlayer.name:<22} {topMoneyPlayer.seasonMoney:>12,.2f} {topMoneyPlayer.name}')

            prizeMoney *= 1.03
            loop += 1

            # Wait.
            time.sleep(1)

        # Stop checking the keyboard.
        self.keyboard.close()



def testPlayerNames():
    ''' Test the player names for duplicates. '''
    player = Player(None)
    for cultureIndex in [0, 1]:
        existingFirstNames = []
        existingLastNames = []
        firstNames, lastNames = player.getNames(cultureIndex)
        numNames = len(firstNames)
        if len(lastNames) > numNames:
            numNames = len(lastNames)
        for nameIndex in range(numNames):
            isFirstName = True
            if nameIndex < len(firstNames):
                firstName = firstNames[nameIndex]
                if firstName in existingFirstNames:
                    isFirstName = False
                else:
                    existingFirstNames.append(firstName)
            else:
                firstName = ''
            isLastName = True
            if nameIndex < len(lastNames):
                lastName = lastNames[nameIndex]
                if lastName in existingLastNames:
                    isLastName = False
                else:
                    existingLastNames.append(lastName)
            else:
                lastName = ''

            print(f'{nameIndex+1:>2} {firstName} {lastName} {"OK" if isFirstName else "Error"} {"OK" if isLastName else "Error"}')



if __name__ == '__main__':
    # Process the command line arguments.
    # This might end the program (--help).
    argParse = argparse.ArgumentParser(prog='sport_of_life', description='Little game to run under Linux and Windows.')
    argParse.add_argument('-n', '--names', help='Test the player names.', action='store_true')
    args = argParse.parse_args()

    # Welcome message.
    print(f'{ansi.RED}Sport Of Life{ansi.RESET_ALL} by Steve Walton 2018-2022.')
    print(f'Python Version {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro} (expecting Python 3).')
    print(f'Operating System is "{platform.system()}".  Desktop is "{os.environ.get("DESKTOP_SESSION")}".')

    isRunProgram = True
    if args.names:
        print('Test the player names.')
        isRunProgram = False
        testPlayerNames()


    #for count in range(10):
    #    # This works on Windows but not in IDLE.
    #    print(count, end='\r', flush=True)
    #
    #    # This does not work in Windows.
    #    # print(count)
    #    # sys.stdout.write("\033[F")
    #
    #    # Wait for a second.
    #    time.sleep(1)

    if isRunProgram:
        # Main loop.
        game = Game()
        game.run()

    print(f'Goodbye from the {ansi.RED}Sport Of Life{ansi.RESET_ALL} program.')

    # Having a problem with modInKey not restoring the echo flag to the terminal.
    # Better to get modInKey working and remove this line.
    # os.system('stty echo')
