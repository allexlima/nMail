class Friendship:
    def __init__(self, db_obj):
        self.__db = db_obj

    def following(self, user_id):
        sql = "SELECT contacts.friend_id, users.user_name AS friend_name, users.user_email AS friend_email, " \
              "exists(SELECT * FROM n_contacts fb WHERE fb.c_user_id = contacts.friend_id AND " \
              "fb.friendship_active = TRUE) AS follow_back FROM  n_contacts contacts JOIN n_users users " \
              "ON users.user_id = contacts.friend_id WHERE contacts.c_user_id = (%s) " \
              "AND contacts.friendship_active = TRUE;"
        params = [user_id]
        return [dict(item) for item in self.__db.query(sql, params, fetch=True)]

    def followers(self, user_id):
        sql = "SELECT contacts.c_user_id, users.user_name, users.user_email, exists(SELECT * FROM n_contacts fb " \
              "WHERE fb.c_user_id = contacts.friend_id AND fb.friendship_active = TRUE) AS followed_by_me " \
              "FROM n_contacts contacts JOIN n_users users ON users.user_id = contacts.c_user_id WHERE " \
              "contacts.friend_id = (%s) AND contacts.friendship_active = TRUE;"
        params = [user_id]
        return [dict(item) for item in self.__db.query(sql, params, fetch=True)]

    def requests_for(self, user_id):
        """
        This method returns a dict of people who requested to follow 'self.user_id' and weren't accepted yet
        :return: dict([{persons_id, persons_name, persons_email}, ...])
        """
        sql = "SELECT contacts.c_user_id AS persons_id, users.user_name AS persons_name, " \
              "users.user_email AS persons_email FROM  n_contacts AS contacts " \
              "LEFT JOIN n_users AS users ON users.user_id = contacts.c_user_id " \
              "WHERE contacts.friend_id = (%s) AND contacts.friendship_active = FALSE;"
        params = [user_id]
        return [dict(item) for item in self.__db.query(sql, params, fetch=True)]

    def send_request(self, user_id, friend_id):
        feedback = False
        if friend_id != user_id:
            sql = "INSERT INTO n_contacts (c_user_id, friend_id) VALUES ((%s), (%s));"
            params = [user_id, friend_id]

            try:
                feedback = self.__db.query(sql, params, commit=True)
            except psql.IntegrityError as e:
                self.__db.write_log("Solicitação já enviada")
        else:
            self.__db.write_log("Você pode pode enviar uma solicitação para você mesmo")
        return feedback

    def accept(self, user_id, persons_id_to_accept):
        sql_1 = "SELECT * FROM n_contacts WHERE friend_id = (%s) AND c_user_id = (%s);"
        sql_2 = "UPDATE n_contacts SET friendship_active = TRUE WHERE friend_id = (%s) AND c_user_id = (%s);"
        params = [user_id, persons_id_to_accept]
        feedback = False

        if len(self.__db.query(sql_1, params, fetch=True)) > 0:
            feedback = self.__db.query(sql_2, params, commit=True)
        else:
            self.__db.write_log("O usuário {} não enviou uma solicitação de amizade ao usuário {}".format(
                persons_id_to_accept, user_id))
        return feedback

    def block(self, user_id, friend_id_to_block):
        sql = "UPDATE n_contacts SET friendship_active = FALSE WHERE c_user_id = (%s) AND friend_id = (%s);"
        params = [user_id, friend_id_to_block]
        return self.__db.query(sql, params, commit=True)

