# -*- coding: utf-8 -*-
"""Filename: tippspiel.py
Author     : Matthias Brettschneider(bmr2lr)
Date       : 16.06.2016

Details :

    Tipp Structure
    {
        u'user': {
            u'gName': 'Matthias',
            u'sName': 'Brettschneider'},
        u'tipp': {
            u'goalsAwayTeam': 1,
            u'goalsHomeTeam': 2},
        u'homeTeamName': u'France',
        u'awayTeamName': u'Romania'
    }

    Json Structure
    {
        u'status': u'FINISHED',
        u'matchday': 1,
        u'_links': {
            u'awayTeam':     {u'href': u'http://api.football-data.org/v1/teams/811' },
            u'self':         {u'href': u'http://api.football-data.org/v1/fixtures/149855'},
            u'homeTeam':     {u'href': u'http://api.football-data.org/v1/teams/773'},
            u'soccerseason': {u'href': u'http://api.football-data.org/v1/soccerseasons/424'}},
        u'result': {
            u'halfTime': {
                u'goalsAwayTeam': 0,
                u'goalsHomeTeam': 0},
            u'goalsAwayTeam': 1,
            u'goalsHomeTeam': 2},
        u'date': u'2016-06-10T19:00:00Z',
        u'homeTeamName': u'France',
        u'awayTeamName': u'Romania'
    }

"""

from __future__ import print_function
import requests


class Tippspiel(object):
    def __init__(self):
        self.__emData = None
        self.__maxGameNameLenOfResults = None

        self.__apiHeader   = {'X-Auth-Token': ''}
        self.__proxy   = {'http': ''}
        self.__apiEndpoint = 'http://api.football-data.org/v1/soccerseasons/424/fixtures'

        self.__matchResults = {}
        self.__fixtures     = []

        self.users          = {}
        self.__matchNames   = []
        self.__userTips     = {}

    def setApiToken(self, _apiToken):
        self.__apiHeader['X-Auth-Token'] = _apiToken

    def setProxy(self, _httpProxy):
        self.__proxy['http'] = _httpProxy

    def __updateResults(self):
        self.__emData   = requests.get(self.__apiEndpoint, headers=self.__apiHeader, proxies=self.__proxy)
        self.__fixtures = sorted(self.__emData.json()['fixtures'],
                                 key=lambda x: x['date'],
                                 reverse=True)
        self.__matchResults = { (x['homeTeamName'] + '-' + x['awayTeamName']):
                                    { 'goalsHomeTeam': x['result']['goalsHomeTeam'],
                                      'goalsAwayTeam': x['result']['goalsAwayTeam'],
                                      'date':          x['date']}
                                for x in self.__fixtures if x['status'] == "FINISHED"}
        self.__maxGameNameLenOfResults = max([len(x) for x in self.__matchResults.keys()])

    def addUser(self, _gName, _sName, _short):
        self.users[_short] = {'gName': _gName, 'sName': _sName}

    def defineMatchNames(self, _homeName, _awayName):
        self.__matchNames.append((_homeName, _awayName))

    def __assignUserTipsWithMatches(self, _user):
        for ((homeTip, guestTip), (homeTeam, guestTeam)) in zip(self.__userTips[_user], self.__matchNames):
            self.users[_user][(homeTeam + "-" + guestTeam)] = {}
            self.users[_user][(homeTeam + "-" + guestTeam)]['tipGoalsHomeTeam'] = homeTip
            self.users[_user][(homeTeam + "-" + guestTeam)]['tipGoalsAwayTeam'] = guestTip
            self.users[_user]['points'] = 0

    def addUserTip(self, _user, _tip):
        try:
            if len(self.__userTips[_user]) >= len(self.__matchNames):
                raise BufferError("cannot add more tips then defined parties")
        except:
            self.__userTips[_user] = []

        self.__userTips[_user].append(_tip)

        if len(self.__userTips[_user]) == len(self.__matchNames):
            self.__assignUserTipsWithMatches(_user)

    def __updateUserPoints(self, _user):
        for match in self.__matchResults.keys():
            goalsHome = self.__matchResults[match]['goalsHomeTeam']
            goalsAway = self.__matchResults[match]['goalsAwayTeam']

            tipHome = self.users[_user][match]['tipGoalsHomeTeam']
            tipAway = self.users[_user][match]['tipGoalsAwayTeam']

            if tipHome == goalsHome and tipAway == goalsAway:
                self.users[_user]['points'] += 2

            elif (goalsHome == goalsAway and tipHome == tipAway) or \
                 (goalsHome  > goalsAway and tipHome  > tipAway) or \
                 (goalsHome  < goalsAway and tipHome  < tipAway):
                self.users[_user]['points'] += 1

    def printUsers(self):
        maxUserKeyLen = max([len(x) for x in self.users.keys()])
        for user in self.users.keys():
            print('(' + user.rjust(maxUserKeyLen) + ')', end=': ')
            print(self.users[user]['gName'], end=' ')
            print(self.users[user]['sName'])

    def __updateAllUserPoints(self):
        for user in self.users.keys():
            self.__updateUserPoints(user)

    def printResults(self):
        self.__updateResults()
        self.__updateAllUserPoints()
        result = []
        for user in self.users.keys():
            result.append(((self.users[user]['points']),
                           self.users[user]['gName'] + " " + self.users[user]['sName']))
        result = sorted(result, key=lambda (a, b): a, reverse=True)

        maxUserNameLen = max([len(x) for (_, x) in result])

        for i, (pts, user) in enumerate(result):
            print(i + 1, end='. ')
            print(user.rjust(maxUserNameLen), end=': ')
            print(str(pts))

    def printStatsOf(self, _user):
        self.__updateResults()
        self.__updateUserPoints(_user)
        wholeName    = self.users[_user]['gName'] + ' ' + self.users[_user]['sName']
        lenLine      = self.__maxGameNameLenOfResults + 18

        print(wholeName.center(lenLine))
        print('-' * lenLine)

        for game in self.__matchResults.keys():
            goalsHome = self.__matchResults[game]['goalsHomeTeam']
            goalsAway = self.__matchResults[game]['goalsAwayTeam']
            tipHome = self.users[_user][game]['tipGoalsHomeTeam']
            tipAway = self.users[_user][game]['tipGoalsAwayTeam']

            if tipHome == goalsHome and tipAway == goalsAway:
                print('+2', end=' ')
            elif (goalsHome == goalsAway and tipHome == tipAway) or \
                 (goalsHome  > goalsAway and tipHome  > tipAway) or \
                 (goalsHome  < goalsAway and tipHome  < tipAway):
                print('+1', end=' ')
            else:
                print('  ', end=' ')

            print(game.replace('-', ' vs. ').rjust(self.__maxGameNameLenOfResults + 4), end=': ')

            print(str(goalsHome) + '-' + str(goalsAway), end=' ')
            print('(' + str(tipHome) + '-' + str(tipAway) + ')')
