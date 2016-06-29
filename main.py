#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#

import logging

from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import RegexHandler

from utils import Configurator
from utils import encode

from worker import Worker

class Helper:
    def __init__(self, worker):
        self.worker = worker

    @staticmethod
    def __sendmessage__(bot, user_id, feedback):
        for raw_text in feedback:
            text = encode(raw_text)
            bot.sendMessage(user_id, text)

    def start(self, bot, update):
        user_id = update.message.from_user.id

        feedback = self.worker.start_dialog(user_id)
        self.__sendmessage__(bot, user_id, feedback)

    def unknown(self, bot, update):
        message = update.message

        text = message.text
        user_id = message.from_user.id

        feedback = self.worker.keep_dialog(user_id, text)
        self.__sendmessage__(bot, user_id, feedback)

def main():

    logging.basicConfig(level=logging.ERROR)

    configurator = Configurator()
    worker = Worker()
    helper = Helper(worker)

    updater = Updater(configurator['token'])
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', helper.start)
    dispatcher.addHandler(start_handler)

    unknown_handler = RegexHandler(r'.*', helper.unknown)
    dispatcher.addHandler(unknown_handler)

    updater.start_polling()

if __name__ == '__main__':
    main()
