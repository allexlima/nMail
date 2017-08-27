import configparser
import psycopg2 as psql
from psycopg2.extras import DictCursor


class PostrgeSQL(object):
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
        except Exception as e:
            self.write_log(e)

    def db_disconnect(self):
        if self.__conn:
            self.__conn.close()

    def query(self, sql, params=None, commit=False, fetch=False):
        feedback = False
        if self.__conn is not None:
            try:
                cursor = self.__conn.cursor(cursor_factory=DictCursor)
                cursor.execute(sql, params)
                if commit is True:
                    self.__conn.commit()
                feedback = cursor.fetchall() if fetch is True else True
                cursor.close()
            except Exception:
                if commit is True:
                    self.__conn.rollback()
                raise
        else:
            self.write_log("É necessário iniciar uma conexão com o banco antes de executar operações")
        return feedback

    def write_log(self, msg):
        self.__log.append(msg)
        print(msg)

    def view_log(self):
        return self.__log
