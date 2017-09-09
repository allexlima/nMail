from flask import jsonify, abort
from flask_restful import Resource, reqparse
from nmail.database import psql, user
from nmail.resources.common import caching


class UserAPI(Resource):
    def __init__(self):
        self.default_msg = ({
            "message": "The server cannot or will not process the request due to an apparent client error",
            "methods": {
                "GET": {
                    "description": "List an user",
                    "syntax": "/api/user/<int:user_id>",
                    "return": "a user info in JSON Object format"
                },
                "POST": {
                    "description": "Create new user. The parameters must be sent through the request body "
                                   "in JSON object format",
                    "syntax": {
                        'user_name': '<string:max_length(50)>',
                        'user_password': '<string>',
                        'user_email': '<string>',
                    },
                    "return": "the created user_id"
                },
                "PUT": {
                    "description": "Update an user info. All body params are optionals",
                    "syntax": {
                        "URI": "/api/user/<int:user_id>",
                        "Body": {
                            'user_name': '<string:max_length(50)>',
                            'user_password': '<string>',
                            'user_email': '<string>',
                            'user_admin': '<boolean>',
                            'user_active': '<boolean>',
                        }
                    },
                    "return": "a user info in JSON Object format"
                }
            }
        }, 400)

    def get(self, user_id=None):
        result = self.default_msg
        if user_id is not None:
            user_data = user.list(user_id)
            result = caching("user_get_" + str(user_id), jsonify(user_data[0])) if len(user_data) > 0 else (None, 204)
        return result

    @staticmethod
    def post():
        parser = reqparse.RequestParser()
        parser.add_argument('user_name', type=str, required=True)
        parser.add_argument('user_password', type=str, required=True)
        parser.add_argument('user_email', type=str, required=True)
        try:
            feedback = jsonify(user_id=user.insert(*tuple(parser.parse_args().values())))
        except psql.IntegrityError:
            feedback = ({"message": "The informed email address is already in use"}, 409)
        return feedback

    @staticmethod
    def put(user_id=None):
        if user_id:
            parser = reqparse.RequestParser()
            parser.add_argument('user_name', type=str)
            parser.add_argument('user_email', type=str)
            parser.add_argument('user_password', type=str)
            parser.add_argument('user_active', type=bool, default=True)
            parser.add_argument('user_admin', type=bool, default=False)
            user.change(user_id, *tuple(parser.parse_args().values()))
            return jsonify(user.list(user_id)[0])
        else:
            abort(400)
