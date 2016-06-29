import shelve

from os import makedirs
from os import path

from os.path import expanduser
from os.path import join
from os.path import exists

STORAGE_DIR = expanduser('~/.buzz_bot/')
STORAGE_PATH = join(STORAGE_DIR, 'persistance')

class Storage:
    def folderize(f):
        def wrapper(self, *args, **kwargs):
            if not exists(STORAGE_DIR):
                makedirs(STORAGE_DIR)
            return f(self, *args, **kwargs)
        return wrapper

    @folderize
    def synchronize(f):
        def wrapper(self, *args, **kwargs):
            with shelve.open(STORAGE_PATH) as db:
                value = f(self, *args, db, **kwargs)
            return value
        return wrapper

    @synchronize
    def obtain_new_user(self, user_id, db):
        user = str(user_id)
        if user in db:
            return False
        else:
            db[user] = ''
            return True
