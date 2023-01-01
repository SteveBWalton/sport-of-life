# -*- coding: utf-8 -*-

'''
Module to implement Player, a class to represent a player in the sport of life program.
'''

# System libraries.
import random



class Player:
    '''
    Class to represent a player in the sport of life program.

    :ivar Database database: The database that this player is stored in.
    :ivar str name: The name of the player.
    :ivar int skill: The skill level of the player.
    :ivar int age: The age of the player.
    '''



    def __init__(self, database):
        '''
        Class constructor for the :py:class:`Player` class.

        :param CDatabase database: Specifies the :py:class:`~modDatabase.CDatabase` database.
        '''
        # The database that this sport is stored in.
        self.database = database
        self.name: str = str()
        self.skill: int = int()
        self.round: int = int()
        self.pts: int = int()
        self.history = []
        self.ranking: int = int()
        self.wins: int = int()
        self.runnerUp: int = int()
        self.worldChampion: int = int()
        self.topRanking: int = int()
        self.age: int = int()
        self.firstWin: int = int()
        self.lastWin: int = int()
        self.skillOffset: int = int()
        self.prizeMoney: int = int()
        self.seasonMoney: int = int()
        self.reset()



    def reset(self):
        ''' Reset the player to the initial state. '''
        self.name = 'No Name'
        self.skill = 500
        self.round = 0
        self.pts = 0
        self.history = []
        self.ranking = 128
        self.wins = 0
        self.runnerUp = 0
        self.worldChampion = 0
        self.topRanking = 0
        self.age = 17
        self.firstWin = None
        self.lastWin = None
        self.skillOffset = 0
        self.prizeMoney = 0
        self.seasonMoney = 0



    def retire(self):
        ''' Returns a retired copy of the player. '''
        retiredPlayer = Player(self.database)
        retiredPlayer.name = self.name
        retiredPlayer.skill = 0
        retiredPlayer.round = 0
        retiredPlayer.pts = 0
        retiredPlayer.history = []
        retiredPlayer.ranking = 9999
        retiredPlayer.wins = self.wins
        retiredPlayer.runnerUp = self.runnerUp
        retiredPlayer.worldChampion = self.worldChampion
        retiredPlayer.topRanking = self.topRanking
        retiredPlayer.age = self.age
        retiredPlayer.firstWin = self.firstWin
        retiredPlayer.lastWin = self.lastWin
        retiredPlayer.prizeMoney = self.prizeMoney

        return retiredPlayer



    def nameWithRanking(self):
        ''' Returns the name with ranking if top 8. '''
        if self.ranking > 16:
            return self.name
        return f'{self.name} ({self.ranking})'



    def nameWithYearRange(self):
        ''' Returns the name with a year range, if available. '''
        if self.firstWin is None:
            return self.name
        if self.firstWin == self.lastWin:
            return f'{self.name} ({self.firstWin})'
        return f'{self.name} ({self.firstWin}-{self.lastWin})'



    def getNames(self, cultureIndex):   # pylint: disable=no-self-use
        ''' Return the list of possible first names and last names in the specified culture. '''
        if cultureIndex == 1:
            # Chinese names.
            firstNames = ['Ding', 'Marco', 'Liang', 'Yan', 'Xiao', 'Li', 'Zhou', 'Cao', 'Junjie', 'Zhang', 'Chen', 'Xu', 'Lyu', 'Yu', 'Tian', 'Mei', 'Zhao']
            lastNames =  ['Junhui', 'Fu', 'Wenbo', 'Bingtao', 'Guodong', 'Hang', 'Yuelong', 'Yupeng', 'Wang', 'Anda',  'Zhe',  'Si', 'Haotian', 'Delu', 'Pengfei', 'Xiwen', 'Xintong']
        else:
            # English names.
            firstNames = ['Steve',  'Fred',  'Stephen', 'Joe', 'Darren', 'Ronnie', 'Mark', 'Alex', 'Shaun', 'Judd', 'Paul', 'Andrew', 'Ray', 'Kyren', 'Neil', 'Barry', 'Stuart', 'Anthony', 'Graeme', 'John', 'Eddie', 'Kirk', 'Cliff', 'Perrie', 'Ricky', 'Jimmy', 'Daniel', 'Tom', 'Nigel', 'Scott', 'Lewis', 'Damon', 'Jim', 'Sebastian', 'Gareth', 'David', 'Michael', 'Robert', 'James', 'Alan', 'Harry', 'Sterling', 'Richard', 'Bjorg', 'Ivan', 'Gary', 'Martin', 'George', 'Oliver', 'Charlie', 'Jack', 'Oscar', 'Henry', 'Tony', 'Brian', 'Glenn']
            lastNames =  ['Walton', 'Davis', 'Hendry', 'Johnson', 'Lumby', 'O\'Sullivan', 'Williams', 'Higgins', 'Murphy','Trump','Walker', 'Jackson', 'Reardon', 'Wilson', 'Robertson', 'Hawkins', 'Bingham', 'McGill', 'Dott', 'Spencer', 'Charlton', 'Stevens', 'Thorburn', 'Mans', 'Walden', 'White', 'Wells', 'Ford', 'Bond', 'Donaldson', 'Hamilton', 'Hill', 'Clark', 'Coe',  'Southgate', 'Coulthard', 'Holt', 'Redford', 'Whale', 'McManus', 'Potter', 'Moss', 'Osman', 'Borg', 'Lendl', 'Newman', 'Freeman', 'Peel', 'Twist', 'Chaplin', 'Black', 'Wilde', 'Kissinger', 'Curtis', 'Robson', 'Hoddle']
        return firstNames, lastNames



    def randomName(self, cultureIndex):
        ''' Give the player a random name. '''
        firstNames, lastNames = self.getNames(cultureIndex)

        firstNameIndex = random.randint(0, len(firstNames)-1)
        lastNameIndex = random.randint(0, len(lastNames)-1)
        self.name = f'{firstNames[firstNameIndex]} {lastNames[lastNameIndex]}'
        if firstNameIndex == lastNameIndex:
            print(f'Boost for {self.name}. ', end='')
            self.skill += 200
            if firstNameIndex == 0 and cultureIndex == 0:
                self.skill += 200
