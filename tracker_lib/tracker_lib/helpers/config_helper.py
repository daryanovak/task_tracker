import json

def get_config():
    try:
        return json.loads(open('config.json', 'r').read())
    except FileNotFoundError:
        return {
            "database.config": {
                "user": "postgres",
                "password": "postgres",
                "host": "localhost",
                "database": "mydb2"
            }
        }