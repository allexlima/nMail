# -*- coding: utf-8 -*-

from flask import Flask

app = Flask(__name__)

app.config.from_pyfile("settings.cfg")
app.config['DB_URI'] = "postgresql://{user}:{password}@{host}:{port}/{db}".format(
    user=app.config['DB_USER'], password=app.config['DB_PASSWORD'],
    host=app.config['DB_HOST'], port=app.config['DB_PORT'],
    db=app.config['DB_NAME'])


@app.route("/")
def hello():
    return "Hello World!"


if __name__ == "__main__":
    print(app.config['SQLALCHEMY_DATABASE_URI'])
    app.run(host=app.config['HOST'], port=app.config['PORT'])
