import pony.orm as orm

from tracker_lib.helpers.config_helper import get_config

config = get_config()
database_config = config['database.config']
db = orm.Database()

db.bind(
    'postgres',
    user=database_config['user'],
    password=database_config['password'],
    host=database_config['host'],
    database=database_config['database']
)




