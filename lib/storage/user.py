from pony.orm import db_session
from lib.models import User
import os
import secrets


@db_session
def get_current_user():
    if os.stat("lib/token").st_size != 0:
        with open("lib/token", "r") as file:
            token = file.readline()
        user = User.get(token=token)
        return user.id

@db_session
def log_in(login, password):
    if os.stat("lib/token").st_size == 0:
        user = User.get(login=login, password=password)
        user.token = secrets.token_urlsafe()
        with open("lib/token", "w+") as file:
            file.writelines(user.token)
        return user.token
    else:
        raise Exception()

@db_session
def sign_up(login, password):
    User(login=login, password=password)


@db_session
def log_out():
    with open('lib/token', 'r+') as file:
        token = file.readline()

    user = User.get(token=token)
    user.token = ""

    with open('lib/token', 'r+') as file:
        file.truncate()

