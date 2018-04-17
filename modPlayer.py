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
        self.name = 'No Name'
        self.skill = 500
        self.round = 0



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
