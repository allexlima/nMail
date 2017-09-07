from database.base import PostrgeSQL
from database.messages import Messages
from database.user import User

from nmail.database.friendship import Friendship

db = PostrgeSQL().db_connect()

user = User(db)
friendship = Friendship(db)
messages = Messages(db)
