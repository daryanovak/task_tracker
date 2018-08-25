import pony.orm as orm
import json
import os

db = orm.Database()
db.bind(
    'postgres',
    user='postgres',
    password='postgres',
    host='localhost',
    database='mydb'
)
# db.bind(provider='sqlite', filename='database.sqlite1', create_db=True)

db.drop_table("Numbers", if_exists=True, with_all_data=True)

#set_sql_debug(True)



