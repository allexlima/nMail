from database.base import PostrgeSQL, psql
from datetime import datetime


class User(PostrgeSQL):
    def list(self, user_id=None):
        sql = "SELECT user_name, user_email, user_registration_date, user_active, user_admin FROM n_users {} " \
              "ORDER BY user_registration_date DESC;"
        id_if_necessary = "WHERE user_id = {}".format(int(user_id)) if user_id else ""
        sql = sql.format(id_if_necessary)
        return [dict(item) for item in self.query(sql, fetch=True)]

    def get_id(self, user_email):
        sql = "SELECT user_id FROM n_users WHERE user_email = (%s);"
        params = [user_email]
        result = self.query(sql, params, fetch=True)
        return result[0]['user_id'] if len(result) > 0 else -1

    def insert(self, name, password, email, active=True, date=str(datetime.now())):
        sql = "INSERT INTO n_users (user_name, user_password, user_email, user_active, user_registration_date) " \
              "VALUES ((%s), (%s), (%s), (%s), (%s));"
        params = [name, password, email, active, date]
        feedback = False

        try:
            if self.query(sql, params, commit=True):
                feedback = self.get_id(email)
        except psql.IntegrityError:
            self.write_log("O e-mail '{0}' já encontra-se em uso".format(email))
        finally:
            return feedback

    def remove(self, user_id):
        sql = "DELETE FROM n_users WHERE user_id = (%s);"
        params = [user_id]

        return self.query(sql, params=params, commit=True)

    def change(self, user_id, new_name=None, new_email=None, new_password=None, is_activated=True, is_admin=False):
        sql = "UPDATE n_users SET "
        params = []
        adds = []
        if new_name:
            adds.append("user_name = (%s)")
            params.append(new_name)
        if new_email:
            adds.append("user_email = (%s)")
            params.append(new_email)
        if new_password:
            adds.append("user_password = (%s)")
            params.append(new_password)
        adds.append("user_active = (%s)")
        params.append(is_activated)
        adds.append("user_admin = (%s)")
        params.append(is_admin)
        params.append(user_id)
        for i, item in enumerate(adds):
            sql += item
            sql += ", " if i < len(adds)-1 else " "
        sql += "WHERE user_id = (%s);"
        return self.query(sql, params, commit=True)

    def login(self, user_email, user_password):
        """Basic login method. It's important say that the password encryption is done by Postgresql,
        through the CHKPASS column type.
        :returns user_id, user_active
        """
        sql = "SELECT user_id, user_active FROM n_users WHERE user_email = (%s) AND user_password = (%s);"
        params = [user_email, user_password]
        result = self.query(sql, params, fetch=True)
        return tuple(result[0]) if len(result) > 0 else -1

    def search(self, name_or_email):
        pass
