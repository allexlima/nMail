from nmail.database.base import PostrgeSQL, psql
from nmail.database.messages import Messages
from nmail.database.user import User
from nmail.database.friendship import Friendship

db = PostrgeSQL()
db.db_config("database/settings.cfg")  # path to 'settings.cfg' from ./nmail/
db.db_connect()

user = User(db)
friendship = Friendship(db)
messages = Messages(db)
