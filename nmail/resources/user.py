from flask import jsonify, request, abort
from flask_restful import Resource
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
                "PUT": "Update an user info",
                "DELETE": "Remove a specific user from the system"
            }
        }, 400)

    def get(self, user_id=None):
        return caching("user_get_" + str(user_id), jsonify(user.list(user_id)[0]))

    def post(self):
        json_data = request.get_json(force=True)
        feedback = ({"message": ":("}, 500)
        try:
            new_id = user.insert(json_data['user_name'], json_data['user_password'], json_data['user_email'])
            feedback = jsonify(user_id=new_id)
        except KeyError as key_name:
            feedback = ({"message": "Missing key {} in your JSON request".format(key_name)}, 400)
        except psql.IntegrityError:
            feedback = ({"message": "The email address '{}' in your JSON request".format(json_data['user_email'])}, 409)
        return feedback
