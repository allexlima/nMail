import configparser
import psycopg2 as psql
from psycopg2.extras import DictCursor


class PostrgeSQL(object):
    def __init__(self):
        self.__conn = None
        self.log = []

    @staticmethod
    def __config():
        aux = configparser.ConfigParser()
        aux.read("database/settings.cfg")
        return tuple(aux['Database'][i] for i in aux['Database'])

    def db_connect(self):
        try:
            self.__conn = psql.connect("user={} password={} dbname={} host={} port={}".format(*self.__config()))
        except Exception as e:
            self.log.append("Erro ao conectar-se ao banco de dados")
            print(e)

    def db_disconnect(self):
        if self.__conn:
            self.__conn.close()

    def query(self, sql, commit=False, fetch=False):
        if self.__conn is not None:
            try:
                cursor = self.__conn.cursor(cursor_factory=DictCursor)
                cursor.execute(sql)
                if commit is True:
                    self.__conn.commit()
                if fetch is True:
                    return cursor.fetchall()
            except psql.InterfaceError as e:
                self.log.append("Erro ao conectar-se ao banco. Conexão indisponível ou encerrada")
                print(e)
        else:
            msg = "É necessário iniciar uma conexão com o banco antes de executar operações"
            self.log.append(msg)
            raise ConnectionError(msg)
