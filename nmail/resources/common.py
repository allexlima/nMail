from flask_restful import Resource
from werkzeug.contrib.cache import SimpleCache

cache = SimpleCache()


def caching(key, value):
    cached = cache.get(key)
    if cached is None:
        cached = value
        cache.set(key, cached, 30*60)
    return cached


class Home(Resource):
    def __init__(self):
        self.message = {"message": "Hello World"}

    def get(self):
        return self.message

    def post(self):
        return self.message
