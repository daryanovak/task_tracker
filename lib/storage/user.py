from pony.orm import db_session
from lib.models import User
import os
import secrets


# user = User.select(lambda p: p.login == login and p.password == password)
# pickled_data = cPickle.dumps(user)
# users = cPickle.loads(pickled_data)
# listsss = list(users)
# print(listsss[0].login)
# print(users)
# user.show()
@db_session
def get_current_user():
    if os.stat("token").st_size != 0:
        with open("token", "r") as file:
            token = file.readline()
        user = User.get(token=token)
        return user.id

@db_session
def log_in(login, password):
    if os.stat("token").st_size == 0:
        user = User.get(login=login, password=password)
        user.token = secrets.token_urlsafe()
        with open("token", "w+") as file:
            file.writelines(user.token)
    else:
        raise Exception()

@db_session
def sign_up(login, password):
    User(login=login, password=password)


@db_session
def log_out():
    with open('token', 'r+') as file:
        token = file.readline()

    user = User.get(token=token)
    user.token = ""

    with open('token', 'r+') as file:
        file.truncate()

