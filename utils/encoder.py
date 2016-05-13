import json

class Encoder(dict):

    def __init__(self, path):
        super(Encoder, self).__init__()
        with open(path) as descriptor:
            self.content = json.load(descriptor)

    def __getitem__(self, index):
        return self.content.get(index, index)[0]


ENCODER = Encoder('./utils/resources/phrases.json')

def encode(text):
    return text.format(**ENCODER)
