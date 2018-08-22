import pony.orm as orm
import json
import os

config = json.loads(open('./config.json', 'r').read())
database_config = config['database.config']
db = orm.Database()
# db.bind(
#     'postgres',
#     user='postgres',
#     password='postgres',
#     host='localhost',
#     database='mydb2'
# )
db.bind(provider='sqlite', filename='database.sqlite1', create_db=True)

db.drop_table("Numbers", if_exists=True, with_all_data=True)

#set_sql_debug(True)



