from . import Storage

class Worker:

    def __init__(self): pass

    def start_dialog(self, user_id):
        return ['{user_comeback}']

    def keep_dialog(self, user_id, message):
        return ['{no_definition}']
