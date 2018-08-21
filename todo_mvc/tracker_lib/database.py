import pony.orm as orm
import json
import os

config = json.loads(open('./config.json', 'r').read())
database_config = config['database.config']
db = orm.Database()
# db.bind(
#     'postgres',
#     user_id=database_config['user_id'],
#     password=database_config['password'],
#     host=database_config['host'],
#     database=database_config['database']
# )
db.bind(provider='sqlite', filename='database.sqlite1', create_db=True)

db.drop_table("Numbers", if_exists=True, with_all_data=True)

#set_sql_debug(True)



