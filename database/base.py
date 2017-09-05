import configparser
import psycopg2 as psql
from psycopg2.extras import DictCursor


class PostrgeSQL:
    def __init__(self):
        self.__conn = None
        self.__log = []

    @staticmethod
    def __config():
        aux = configparser.ConfigParser()
        aux.read("database/settings.cfg")
        return tuple(aux['Database'][i] for i in aux['Database'])

    def db_connect(self):
        try:
            self.__conn = psql.connect("user={} password={} dbname={} host={} port={}".format(*self.__config()))
        except Exception as error:
            print(error)
        finally:
            return self if self.__conn else None

    def db_disconnect(self):
        return self.__conn.close() if self.__conn else False

    def query(self, sql, params=None, commit=False, fetch=False):
        feedback = None
        try:
            cursor = self.__conn.cursor(cursor_factory=DictCursor)
            cursor.execute(sql, params)
            if commit is True:
                self.__conn.commit()
            feedback = cursor.fetchall() if fetch is True else None
            cursor.close()
        except Exception:
            if commit is True:
                self.__conn.rollback()
            raise
        finally:
            return feedback
