#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#

import json
import logging

from database import Database
from encoder import Encoder

import telegram
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import RegexHandler

class Node:

    def __init__(self, name):
        self.map = {}
        self.name = name

    def add_adj(self, message, node, feedback):
        self.map[message] = node, feedback

    def go(self, message):
        return self.map.get(message, self.map.get(''))

class Graph:

    def __init__(self, cur_node_name):
        self.nodes = {}

        napping = self.add_node('napping')
        idle = self.add_node('idle')
        activity = self.add_node('activity')
        decision = self.add_node('decision')

        self.add_edge(napping, idle, '/wake',
                      lambda: ['{wake}'])

        self.add_edge(idle, napping, '/snooze', \
                      lambda: ['{snooze}'])

        self.add_edge(idle, decision, '/do',
                      lambda: ['{decision}'])

        self.add_edge(decision, idle, '/cancel',
                      lambda: ['{no_decision}'])

        self.add_edge(decision, activity, '',
                      lambda: ['{activity}'])

        self.add_edge(activity, idle, '/done',
                      lambda: ['{activity_is_done}'])

        self.cur_node = self.nodes[cur_node_name]

    def add_node(self, name):
        node = Node(name)
        self.nodes[name] = node
        return node

    def add_edge(self, src, dst, message, feedback):
        src.add_adj(message, dst, feedback)

    def go(self, msg):
        self.cur_node, feedback = self.cur_node.go(msg)
        return self.cur_node.name, feedback()

class Configuration:

    def __init__(self, path='./configuration.json'):
        with open(path) as f:
            data = json.load(f)
            f.close()

        self.token = data['token']
        self.resources = data['resources']

config = Configuration()
db = Database(config.resources + '/database.sqlite')
encoder = Encoder('./phrases.json')

def start_converstation(user_id):
    if db.contains(user_id):
        return '{user_comeback}'
    else:
        logging.info('{0} tries to chat'.format(user_id))
        db.add_user(user_id)
        return '{new_user}'

def start(bot, update):
    user_id = update.message.from_user.id
    text_to_send = encode(start_converstation(user_id))
    bot.sendMessage(user_id, text_to_send)

def encode(raw_text):
    try:
        return raw_text.format(**encoder)
    except:
        return raw_text

def continue_conversation(user_id, text):
    node = db.get_user_node(user_id)
    graph = Graph(node)

    try:
        new_node, feedback = graph.go(text)
        db.add_activity(user_id, text, new_node)
        return feedback
    except Exception as e:
        logging.debug('try except block failed: %s', e)
        return ['{not_valid}']

def unknown(bot, update):
    message = update.message
    user_id = message.from_user.id
    bot.sendChatAction(user_id,
                       telegram.ChatAction.TYPING)
    text = message.text
    messages = continue_conversation(user_id, text)
    for raw_text in messages:
        bot.sendMessage(user_id, encode(raw_text))


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
