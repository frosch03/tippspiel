# -*- coding: utf-8 -*-
"""Filename : command_line.py
Author      : Matthias Brettschneider(bmr2lr)
Date        : 17.06.2016

Details : This file contains the main function for the delivered
application. Here the command line parser is configured 
"""
from os.path import expanduser

import argparse
import yaml

from tippspiel import Tippspiel


def readInConfig(_ts, config=expanduser("~") + '/.tipconfig.yml'):
    with open(config, 'r') as ymlfile:
        cfg = yaml.load(ymlfile)

    # Set the API-Key of the DataProvider
    _ts.setApiToken(cfg['Game']['DataProvider']['ApiKey'])

    # Set your Proxy-Configuration if you need any
    _ts.setProxy(cfg['Game']['DataProvider']['Proxy'])

    # Read in the match configuration
    for home, away in cfg['Game']['Event']['Matches']:
        _ts.defineMatchNames(home, away)

    # Read in the user-specific configuration (names and shortnames
    # and tips)
    for user in cfg['Game']['Users'].keys():
        gName = cfg['Game']['Users'][user]['givenName']
        sName = cfg['Game']['Users'][user]['sureName']
        _ts.addUser(gName, sName, user)

        # tips = [tuple(tip) for tip in cfg['Game']['Users'][user]['tips']]
        for tip in cfg['Game']['Users'][user]['tips']:
            _ts.addUserTip(user, tuple(tip))


def main():
    ts = Tippspiel()

    parser = argparse.ArgumentParser(description='Track the state of a football tip game')
    parser.add_argument('-c', '--config',  dest='configFile', help='use the given game configureation')
    parser.add_argument(      '--users',   dest='showUsers',  help='list the participating users',       action='store_true')
    parser.add_argument(      '--table',   dest='showTable',  help='print the scores table',             action='store_true')
    parser.add_argument(      '--of',      dest='userShort',  help='print the points per game and user', nargs=1)  # , choices=(ts.users.keys()))

    args = parser.parse_args()

    # Read in configuration given location, else search for a config
    # at a default location
    if args.configFile is None:
        readInConfig(ts)
    else:
        readInConfig(ts, config=args.configFile)

    if args.showUsers:
        ts.printUsers()

    elif args.showTable:
        ts.printResults()

    elif args.userShort is None:
        parser.print_help()

    elif args.userShort[0] in ts.users.keys():
        ts.printStatsOf(args.userShort[0])

    exit(0)
