class Messages:
    def __init__(self, db_obj):
        self.__db = db_obj

    def send(self, from_user_id, to_user_id, msg_content, msg_title):
        sql = "INSERT INTO n_messages (msg_title, msg_content, send_datetime, user_sender, user_receiver) " \
              "VALUES ((%s), (%s), now(), (%s), (%s));"
        params = [msg_title, msg_content, from_user_id, to_user_id]
        return self.__db.query(sql, params, commit=True)

    def send_as_system(self, to_user_id, msg_title, msg_content):
        sql = "INSERT INTO n_messages (msg_title, msg_content, send_datetime, user_receiver, from_system) " \
              "VALUES ((%s), (%s), now(), (%s), True);"
        params = [msg_title, msg_content, to_user_id]
        return self.__db.query(sql, params, commit=True)

    def list_received(self, user_id):
        sql = "SELECT * FROM n_messages WHERE user_receiver = (%s) ORDER BY msg_id DESC;"
        params = [user_id]
        return [dict(item) for item in self.__db.query(sql, params, fetch=True)]

    def list_sent(self, user_id):
        sql = "SELECT * FROM n_messages WHERE user_sender = (%s) ORDER BY msg_id DESC;"
        params = [user_id]
        return [dict(item) for item in self.__db.query(sql, params, fetch=True)]

    def read(self, msg_id, viewed=True):
        sql = "UPDATE n_messages SET msg_viewed = TRUE WHERE msg_id = (%s);"
        params = [True if viewed else False]
        return self.__db.query(sql, params, commit=True)

    def delete(self, msg_id):
        sql = "DELETE FROM n_messages WHERE msg_id = (%s);"
        params = [msg_id]
        return self.__db.query(sql, params, commit=True)
