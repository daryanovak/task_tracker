import pony.orm as orm

db = orm.Database()
db.bind(
    'postgres',
    user='postgres',
    password='postgres',
    host='localhost',
    database='users'
)

db.drop_table("Numbers", if_exists=True, with_all_data=True)




