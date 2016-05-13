import json

class Encoder(dict):

    def __init__(self, path):
        dict.__init__()
        with open(path) as descriptor:
            self.content = json.load(descriptor)

    def __getitem__(self, index):
        return self.content.get(index, index)


ENCODER = Encoder('./utils/resources/phrases.json')

def encode(text):
    return text.format(**ENCODER)
