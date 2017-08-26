# -*- coding: utf-8 -*-

import psycopg2 as psql
from datetime import datetime


class Database(object):
    def __init__(self, user, password, db_name='n_mail', host='localhost', port=5432):
        self.user = user
        self.password = password
        self.db_name = db_name
        self.host = host
        self.port = port
        self.__conn = None
        self.log = []

    def connect(self):
        ps_dsn = "user={} password={} dbname={} host={} port={}".format(self.user, self.password, self.db_name,
                                                                        self.host, self.port)
        try:
            self.__conn = psql.connect(ps_dsn)
        except psql.Error as e:
            print(e)

    def disconnect(self):
        if self.__conn:
            self.__conn.close()

    def run(self, query, commit=False, fetch=False):
        if self.__conn is not None:
            cursor = self.__conn.cursor()
            cursor.execute(query)
            if commit is True:
                self.__conn.commit()
            if fetch is True:
                return cursor.fetchall()
        else:
            msg = "Erro ao conectar-se ao banco de dados"
            self.log.append(msg)
            raise Exception(msg)

    def insert_user(self, name, password, email, date=str(datetime.now())):
        query = "INSERT INTO n_users (user_name, user_password, user_email, user_registration_date) VALUES (" \
                "'{}', '{}', '{}', '{}');".format(name, password, email, date)

        user_id = None

        try:
            self.run(query, commit=True)
            user_id = self.run("SELECT user_id FROM n_users WHERE user_email = '{}';".format(email), fetch=True)
        except psql.IntegrityError:
            msg = "O e-mail '{}' já encontra-se em uso".format(email)
            self.log.append(msg)
            print(msg)
        except Exception as error:
            print(error)

        return user_id[0][0] if user_id else -1

    def list_user(self, user_id=None):
        pass


if __name__ == "__main__":
    test = Database('allex', 'allex')
    test.connect()
    id = test.insert_user('Fulano', '123', 'fulando@gmail.com')
    print(id)
