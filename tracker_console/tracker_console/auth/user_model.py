from tracker_console.auth.user_database import db
from pony.orm import *


class User(db.Entity):
    id = PrimaryKey(int, auto=True)
    login = Required(str, unique=True)
    password = Required(int)
    token = Optional(LongStr)


db.generate_mapping(create_tables=True)
