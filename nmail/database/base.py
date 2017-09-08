import configparser
import psycopg2 as psql
from psycopg2.extras import DictCursor


class PostrgeSQL:
    def __init__(self):
        self.__conn = None
        self.__log = []
        self.__config = None

    def db_config(self, file="settings.cfg"):
        aux = configparser.ConfigParser()
        aux.read(file)
        self.__config = tuple(aux['Database'][i] for i in aux['Database'])

    def db_connect(self):
        self.__conn = psql.connect("user={} password={} dbname={} host={} port={}".format(*self.__config))
        return self

    def db_disconnect(self):
        return self.__conn.close() if self.__conn.status else False

    def query(self, sql, params=None, commit=False, fetch=False):
        feedback = None
        try:
            cursor = self.__conn.cursor(cursor_factory=DictCursor)
            cursor.execute(sql, params)
            feedback = cursor.fetchall() if fetch is True else None
            if commit is True:
                self.__conn.commit()
                feedback = True if feedback is None else feedback
            cursor.close()
        except Exception:
            if commit is True:
                self.__conn.rollback()
            raise
        return feedback
