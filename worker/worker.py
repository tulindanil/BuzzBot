from . import Storage

class Edge():
    def __init__(self, neighbor, feedback):
       self.neighbor = neighbor
       self.feedback = feedback

class Node():
    def __init__():
        self.map = {}

    def add_neighbor(key, edge):
        self.map[key] = edge

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

        for from_idx, to_idx, key, feedback in edges:
            node_name = node_names[from_idx]
            neighbor_name = node_names[to_idx]

            node = self.nodes[node_name]
            neighbor = self.nodes[neighbor_name]

            edge = Edge(neighbor, feedback)
            node.add_neighbor(key, edge)

        self.initial_node = self.nodes[node_names[1]]
        self.current_node = self.initial_node

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
