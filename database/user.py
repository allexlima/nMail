from database.base import PostrgeSQL, psql
from datetime import datetime


class User(PostrgeSQL):
    def show(self, user_id=None):
        sql = "SELECT user_name, user_email, user_registration_date, user_admin FROM n_users {} ORDER BY " \
                "user_registration_date DESC;"
        id_if_necessary = "WHERE user_id = {}".format(int(user_id)) if user_id else ""
        sql = sql.format(id_if_necessary)
        return self.query(sql, fetch=True)

    def insert(self, name, password, email, date=str(datetime.now())):
        sql = "INSERT INTO n_users (user_name, user_password, user_email, user_registration_date) VALUES (" \
                "'{}', '{}', '{}', '{}');".format(name, password, email, date)

        user_id = None

        try:
            self.query(sql, commit=True)
            user_id = self.run("SELECT user_id FROM n_users WHERE user_email = '{}';".format(email), fetch=True)
        except psql.IntegrityError:
            msg = "O e-mail '{}' já encontra-se em uso".format(email)
            self.log.append(msg)
            print(msg)
        except Exception as error:
            print(error)

        return user_id[0]['user_id'] if user_id else -1

    def remove(self, user_id):
        sql = ""