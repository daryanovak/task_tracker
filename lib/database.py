from pony.orm import *

#set_sql_debug(True)

db = Database()

db.bind('sqlite', 'test_.sqlite', create_db=True)
# db.bind('postgres', users='postgres', password='postgres', host='localhost', database='mydb')

db.drop_table("Numbers", if_exists=True, with_all_data=True)

