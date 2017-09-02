from datababse.base import PostrgeSQL, psql


class Friendship(PostrgeSQL):
    def __init__(self, user_id):
        self.user_id = user_id

    def list(self, accepted=True):
        pass

    def check(self, friend_id):
        pass

    def request(self, friend_id):
        sql = "INSERT INTO n_contacts (c_user_id, friend_id) VALUES ((%s), (%s));"
        params = [self.user_id, friend_id]
        feedback = False

        try:
            feedback = self.query(sql, params, commit=True)
        except psql.IntegrityError as e:
            self.write_log("Solicitação já enviada")
        finally:
            return feedback

    def accept(self, friend_id):
        pass

    def block(self, friend_id):
        pass
