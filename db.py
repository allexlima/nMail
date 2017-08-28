from database.user import User
from database.base import PostrgeSQL

import json

if __name__ == "__main__":
    user = User()
    user.db_connect()
    # user.change(34, new_name='Allex Lima', is_admin=True, is_activated=True)
    print(user.search('allex'))
