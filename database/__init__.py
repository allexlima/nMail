from database.base import PostrgeSQL
from database.user import User
from database.friendship import Friendship
from database.messages import Messages

db = PostrgeSQL().db_connect()

user = User(db)
friendship = Friendship(db)
messages = Messages(db)
