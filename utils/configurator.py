import json

class Configurator:

    def __init__(self, path='./.credentials.json'):
        self.read_content(path)

    def __getitem__(self, index):
        return self.content[index]

    def read_content(self, path):
        with open(path) as descriptor:
            content = json.load(descriptor)
            self.content = content
