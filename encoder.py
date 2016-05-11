import json

from random import randint

class Encoder(dict):

    def __init__(self, path):
        self.path = path
        with open(path) as f:
            self.content = json.load(f)

    def __getitem__(self, key):
        arr = self.content[key]
        length = len(arr)
        return arr[randint(0, length - 1)]
