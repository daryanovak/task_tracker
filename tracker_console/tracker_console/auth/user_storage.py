from pony.orm import db_session
from tracker_console.auth.user_model import User
import secrets
import logging

logger = logging.getLogger('logger')


@db_session
def get_user(token: str):
    if not token:
        return None
    user = User.get(token=token)
    return user


@db_session
def log_in(login, password):
    user = User.get(login=login, password=password)
    user.token = secrets.token_urlsafe()
    logger.info('User %s login' % user.login)
    return user.token


@db_session
def sign_up(login, password):
    User(login=login, password=password)
    logger.info('User %s sign_up' % login)


@db_session
def log_out(user_id):
    user = User.get(id=user_id)
    user.token = ""
    logger.info('User %s log out' % user.login)

