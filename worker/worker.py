from . import Storage

class Node():
    def __init__():
        self.map = {}

    def add_neighbor(to_node, cmd, feedback):
        pass

class Graph():
    def __init__(self):
        node_names = ['napping', 'idle',
                      'activity', 'decision']

        edges = [(0, 1, '/wake', '{wake}'),
                 (1, 0, '/snooze', '{snooze}'),
                 (1, 3, '/do', '{decision}'),
                 (3, 1, '/cancel', '{no_decision}'),
                 (3, 2, '', '{activity}'),
                 (2, 1, '/done', '{activity_is_done}')]

        self.nodes = {}
        for name in node_names:
            self.nodes[name] = Node()

        for from_idx, to_idx, cmd, feedback in edges:
            from_node = self.nodes[from_idx]
            to_node = self.nodes[to_idx]
            node.add_neighbor(to_node, cmd, feedback)

        self.current_node = self.nodes[node_names[1]]

class Worker:
    def __init__(self):
        self.storage = Storage()

    def start_dialog(self, user_id):
        if self.storage.obtain_new_user(user_id):
            return ['{new_user}']
        else:
            return ['{user_comeback}']

    def keep_dialog(self, user_id, message):
        return ['{no_definition}']
