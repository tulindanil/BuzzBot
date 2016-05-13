#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#

import json                                                 
import logging

import sys

from database import Database
from encoder import Encoder

import telegram
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import RegexHandler

from configurator import configurator

def main():

    logging.basicConfig(level=logging.DEBUG)

    c = configurator()

    updater = Updater(c['token'])
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)
    dispatcher.addHandler(start_handler)

    unknown_handler = RegexHandler(r'.*', unknown)
    dispatcher.addHandler(unknown_handler)

    updater.start_polling()

if __name__ == '__main__':

    while 1:
        try: main()
        except KeyboardInterrupt:
            sys.exit(0)
        except Exception as e:
            print('Caught exception',
                  'in the main loop:',
                  '%s' % e)
