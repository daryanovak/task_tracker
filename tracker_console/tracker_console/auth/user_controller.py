import tracker_console.auth.user_storage as user_storage


class UserController:
    def sign_up(self, login: str, password: str):
        """
        Creates a new user_id
        :param login:
        :param password:
        """
        user_storage.sign_up(login=login, password=password)

    def log_in(self, login: str, password: str):
        """
        Log_in user_id with such login and password
        :param login:
        :param password:
        """
        return user_storage.log_in(login=login, password=password)

    def log_out(self, user_id):
        """
        Log_out current authorization user_id
        """
        user_storage.log_out(user_id)

    def is_authorized(self, token):
        """
        Checks if user is authorized
        :param token: token file, which storage unique information about authorized user
        :return:
        """
        return not not user_storage.get_user(token)

    def user_id(self, token):
        user = user_storage.get_user(token)
        if user:
            return user.id
        else:
            return -1


