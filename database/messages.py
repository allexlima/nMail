class Messages:
    def __init__(self, db_obj):
        self.__db = db_obj

    def send(self, from_user_id, to_user_id, msg_title, msg_content):
        pass

    def send_as_system(self, to_user_id, msg_title, msg_content):
        pass

    def list(self, user_id):
        pass

    def read(self, msg_id, viewed=True):
        pass

    def viewed_status(self, status):
        pass

    def delete(self, msg_id):
        pass
