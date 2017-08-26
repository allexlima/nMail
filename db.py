from database.user import User
from database.base import PostrgeSQL

import json

if __name__ == "__main__":
    a = User()
    a.db_connect()
    print(a.show())


