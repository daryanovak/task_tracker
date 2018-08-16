import lib.storage.user as user_storage
import os


class UserController:
    def sign_up(self, login, password):
        user_storage.sign_up(login=login, password=password)

    def log_in(self, login, password):
        user_storage.log_in(login=login, password=password)

    def log_out(self):
        user_storage.log_out()

