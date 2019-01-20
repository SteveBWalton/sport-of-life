# -*- coding: utf-8 -*-

'''
Module to implement CPlayer, a class to represent a player in the sport of life program.
'''

# Require the Sqlite3 library
try:
    import sqlite3
except:
    print("pysqlite is not available");
    print("Try package python-sqlite2");
    sys.exit(1)
import random


class CPlayer:
    '''
    Class to represent a player in the sport of life program.

    :ivar CDatabase database: The database that this sport is stored in.
    :ivar int index: The key index of the sport. -1 for a new record. Linked to the 'ID' field.
    :ivar string name: The name of the sport.
    :ivar string singular: The label for a singular team in the sport.  Eg. team, player.
    :ivar string plural: The label for a plural team in the sport.  Eg. teams, players.
    :ivar bool table_nations: True if the sport supports a table of nations.
    :ivar bool seeded_teams: True if the sport supports seeds in the tournaments.  Expected to be false.
    '''



    def __init__(self, Database):
        '''
        Class constructor for the :py:class:`CPlayer` class.

        :param CDatabase Database: Specifies the :py:class:`~modDatabase.CDatabase` database.
        '''
        # The database that this sport is stored in.
        self.database = Database
        self.Reset()



    def Reset(self):
        ''' Reset the player to the initial state. '''
        self.name = 'No Name'
        self.skill = 500
        self.round = 0
        self.pts = 0
        self.history = []
        self.ranking = 128
        self.wins = 0
        self.runner_up = 0
        self.world_champion = 0
        self.top_ranking = 0
        self.age = 17
        self.first_win = None
        self.last_win = None
        self.skill_offset = 0
        self.prize_money = 0
        self.season_money = 0



    def Retire(self):
        ''' Returns a retired copy of the player. '''
        oRetiredPlayer = CPlayer(self.database)
        oRetiredPlayer.name = self.name
        oRetiredPlayer.skill = 0
        oRetiredPlayer.round = 0
        oRetiredPlayer.pts = 0
        oRetiredPlayer.history = []
        oRetiredPlayer.ranking = 9999
        oRetiredPlayer.wins = self.wins
        oRetiredPlayer.runner_up = self.runner_up
        oRetiredPlayer.world_champion = self.world_champion
        oRetiredPlayer.top_ranking = self.top_ranking
        oRetiredPlayer.age = self.age
        oRetiredPlayer.first_win = self.first_win
        oRetiredPlayer.last_win = self.last_win
        oRetiredPlayer.prize_money = self.prize_money

        return oRetiredPlayer



    def NameWithRanking(self):
        ''' Returns the name with ranking if top 8. '''
        if self.ranking > 16:
            return self.name
        return '{} ({})'.format(self.name, self.ranking)



    def NameWithYearRange(self):
        ''' Returns the name with a year range, if available. '''
        if self.first_win == None:
            return self.name
        if self.first_win == self.last_win:
            return '{} ({})'.format(self.name, self.first_win)
        return '{} ({}-{})'.format(self.name, self.first_win, self.last_win)



    def _GetNames(self, nCulture):
        ''' Return the list of possible first names and last names in the specified culture. '''
        if nCulture == 1:
            # Chinese names.
            FirstNames = ['Ding', 'Marco', 'Liang', 'Yan', 'Xiao', 'Li', 'Zhou', 'Cao', 'Junjie', 'Zhang', 'Chen', 'Xu', 'Lyu', 'Yu', 'Tian', 'Mei', 'Zhao']
            LastNames =  ['Junhui', 'Fu', 'Wenbo', 'Bingtao', 'Guodong', 'Hang', 'Yuelong', 'Yupeng', 'Wang',   'Anda',  'Zhe',  'Si', 'Haotian', 'Delu', 'Pengfei', 'Xiwen', 'Xintong']
        else:
            # English names.
            FirstNames = ['Steve',  'Fred',  'Stephen', 'Joe', 'Darren', 'Ronnie', 'Mark', 'Alex', 'Shaun', 'Judd', 'Paul', 'Andrew', 'Ray', 'Kyren', 'Neil', 'Barry', 'Stuart', 'Anthony', 'Graeme', 'John', 'Eddie', 'Kirk', 'Cliff', 'Perrie', 'Ricky', 'Jimmy', 'Daniel', 'Tom', 'Nigel', 'Scott', 'Lewis', 'Damon', 'Jim', 'Sebastian', 'Gareth', 'David', 'Michael', 'Robert', 'James', 'Alan', 'Harry', 'Sterling', 'Richard', 'Bjorg', 'Ivan', 'Gary', 'Martin', 'George', 'Oliver', 'Charlie', 'Jack', 'Oscar', 'Henry']
            LastNames =  ['Walton', 'Davis', 'Hendry', 'Johnson', 'Lumby', 'O\'Sullivan', 'Williams', 'Higgins', 'Murphy','Trump','Walker', 'Jackson', 'Reardon', 'Wilson', 'Robertson', 'Hawkins', 'Bingham', 'McGill', 'Dott', 'Spencer', 'Charlton', 'Stevens', 'Thorburn', 'Mans', 'Walden', 'White', 'Wells', 'Ford', 'Bond', 'Donaldson', 'Hamilton', 'Hill', 'Clark', 'Coe',  'Southgate', 'Coulthard', 'Holt', 'Redford', 'Whale', 'McManus', 'Potter', 'Moss', 'Osman', 'Borg', 'Lendl', 'Newman', 'Freeman', 'Peel', 'Twist', 'Chaplin', 'Black', 'Wilde', 'Kissinger']
        return FirstNames, LastNames



    def RandomName(self, nCulture):
        ''' Give the player a random name. '''
        FirstNames, LastNames = self._GetNames(nCulture)

        nFirstNameIndex = random.randint(0, len(FirstNames)-1)
        nLastNameIndex = random.randint(0, len(LastNames)-1)
        self.name = '{} {}'.format(FirstNames[nFirstNameIndex], LastNames[nLastNameIndex])
        if nFirstNameIndex == nLastNameIndex:
            print('Boost for {}. '.format(self.name), end='')
            self.skill += 200
            if nFirstNameIndex == 0 and nCulture == 0:
                self.skill += 200



    def Read(self, SportID):
        '''
        Read this sport from the database.

        :param int SportID: Specifies the ID of the sport to read from the database.
        '''
        # Lookup the specified sport.
        cndb = sqlite3.connect(self.database.filename)
        cursor = cndb.execute('SELECT Name, Singular, Plural, TableOfNations, ShowFlags, RUNNERSUP, SHOWSCORE, Birthdates, TeamRetire, WindowColumns, Detail, TeamsForgotten, MatchResults, PTS_DEC_PLACES, SEEDED_TEAMS FROM Sports WHERE ID={};'.format(SportID))
        oRow = cursor.fetchone()
        cursor.close()

        self.index = SportID
        if oRow != None:
            self.name = oRow[0]
            self.singular = oRow[1]
            self.plural = oRow[2]
            self.table_nations = oRow[3]
            self.show_flags = oRow[4]
            self.runners_up = oRow[5]
            self.show_score = oRow[6]
            self.birthdates = oRow[7]
            self.teams_retire = oRow[8]
            self.window_columns = oRow[9]
            self.details = oRow[10]
            self.last_year_padding = oRow[11]
            self.match_result_options = oRow[12]
            self.pts_dec_places = 0 if oRow[13]==None else oRow[13]
            self.seeded_teams = oRow[14]

        # Close the database.
        cndb.close()

        # Get the tournaments for this sport.
        self.LoadTournaments()

        # Get the flags for this sport.
        self.LoadFlags()

        self.GetYearRange()



    def Write(self):
        ''' Update this sport in the database. '''
        # Open the database.
        cndb = sqlite3.connect(self.database.filename)

        # Write the settings into this sport.
        if self.index != -1:
            sql = 'UPDATE Sports SET Name = ?, Singular = ?, Plural = ?, Birthdates = ?, TeamRetire = ?, ShowScore = ?, ShowFlags = ?, TableOfNations = ?, TeamsForgotten = ?, MatchResults = ?, WindowColumns = ?, Detail = ?, PTS_DEC_PLACES = ?, SEEDED_TEAMS = ? WHERE ID = ?;'
            params = (self.name, self.singular, self.plural, 1 if self.birthdates else 0, 1 if self.teams_retire else 0, 1 if self.show_score else 0, 1 if self.show_flags else 0, 1 if self.table_nations else 0, self.last_year_padding, self.match_result_options, self.window_columns, self.details, self.pts_dec_places, 1 if self.seeded_teams else 0, self.index)
        else:
            # Find the ID for a new record.
            sql = 'SELECT MAX(ID) FROM SPORTS'
            cursor = cndb.execute(sql)
            oRow = cursor.fetchone()
            cursor.close()
            self.index = oRow[0] + 1

            # Create a new record.
            sql = 'INSERT INTO Sports (ID, Name, Singular, Plural, Birthdates, TeamRetire, ShowScore, ShowFlags, TableOfNations, TeamsForgotten, MatchResults, WindowColumns, Detail, PTS_DEC_PLACES, SEEDED_TEAMS) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);'
            params = (self.index, self.name, self.singular, self.plural, 1 if self.birthdates else 0, 1 if self.teams_retire else 0, 1 if self.show_score else 0, 1 if self.show_flags else 0, 1 if self.table_nations else 0, self.last_year_padding, self.match_result_options, self.window_columns, self.details, self.pts_dec_places, 1 if self.seeded_teams else 0)
        if self.database.debug:
            print(sql)
        cursor = cndb.execute(sql, params)
        cndb.commit()

        # Close the database.
        cndb.close()

        # Return success.
        return True
