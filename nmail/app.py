from flask import Flask
from flask_restful import Api

from nmail.resources.common import Home
from nmail.resources.user import UserAPI

app = Flask("nmail")
api = Api(app, catch_all_404s=True)

api.add_resource(Home, '/', '/index', '/default', '/home', '/api')
api.add_resource(UserAPI, '/api/user', '/api/user/<int:user_id>')
