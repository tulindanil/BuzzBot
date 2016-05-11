#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#

import json
import logging

import telegram
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import RegexHandler

class Node:

    def __init__(self):
        self.map = {}

    def add_adj(self, message, node, feedback):
        self.map[message] = node, feedback

    def go(self, message):
        return self.map.get(message, 
                            self.map.get(''))

class Graph:

    def __init__(self):
        self.nodes = {}

        self.add_node('napping')
        self.add_node('idle')
        self.add_node('activity')
        self.add_node('decision')

        self.add_edge('napping', 'idle', '/wake', 
                      'It was really nice, I suppose')

        self.add_edge('idle', 'napping', '/snooze', \
                      'Yo, man. I got it.' + 
                      ' Nap time is the best solution')

        self.add_edge('idle', 'decision', '/do', 
                      'What are you gonna do?')

        self.add_edge('decision', 'idle', '/cancel', 
                      'Keep idling, bitch')

        self.add_edge('decision', 'activity', '',
                      'Do it, man!')

        self.add_edge('activity', 'idle', '/done', 
                      'Nice work, man!')

        self.cur_node = self.nodes['idle']

    def add_node(self, name):
        self.nodes[name] = Node()

    def add_edge(self, src, dst, message, feedback):
        self.nodes[src].add_adj(message, self.nodes[dst], feedback)

    def go(self, msg):
       self.cur_node, feedback = self.cur_node.go(msg)
       return feedback

class Configuration:

    def __init__(self, path='./configuration.json'):

        with open(path) as f:
            data = json.load(f)
            f.close()

        self.token = data['token']
        self.resources = data['resources']

config = Configuration()

def start(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id,  \
                    text="I'm a bot, please talk to me!")

graph = Graph()

def unknown(bot, update):
    text = update.message.text 
    chat_id = update.message.chat_id
    try: 
        cmd, = text.split()
        feedback = graph.go(cmd)
        bot.sendMessage(chat_id, feedback)
    except Exception as e:
        logging.debug('Can\'t go in the graph: {0}'.format(e))
        bot.sendMessage(chat_id, \
                        'Heeey, that is not valid')

if __name__ == '__main__':

    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    updater = Updater(token=config.token)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)
    dispatcher.addHandler(start_handler)

    unknown_handler = RegexHandler(r'.*', unknown)
    dispatcher.addHandler(unknown_handler)

    updater.start_polling()
