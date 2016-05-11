import sqlite3
from datetime import datetime

class Database:

    def __init__(self, path):
        
        self.path = path

        with sqlite3.connect(path) as conn:
            c = conn.cursor()
            c.execute('create table if not exists users' + \
                      '(id int not null unique primary key, node ntext not null)')
            conn.commit()

    def add_user(self, user_id):
        with sqlite3.connect(self.path) as conn:
            c = conn.cursor()
            t = (user_id, )
            c.execute('insert into users values(?, "idle")', t)
            c.execute('create table if not exists user_{0}'.format(user_id) + \
                      '(activity ntext not null, time smalldatetime not null)')
            conn.commit()

    def add_activity(self, user_id, activity, new_node):
        t = (activity, str(datetime.now()))
        self.__execute__('insert into user_{0} '.format(user_id) + \
                         'values(?, ?)', *t)
        self.__execute__('update users set node=(?) where id=(?)', 
                         new_node, user_id)

    def get_user_node(self, user_id):
        cmd = 'select node from users where id=(?)'
        node, = self.__execute__(cmd, user_id) 
        return node 

    def contains(self, user_id):
        data = self.__execute__('select * from users where id=(?)', 
                                user_id)
        return data and len(data) != 0

    def __execute__(self, cmd, *args):
        with sqlite3.connect(self.path) as conn:
            c = conn.cursor()
            c.execute(cmd, args)
            data = c.fetchone()
            conn.commit()
        return data
