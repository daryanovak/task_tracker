import json
import tracker_lib.helpers.errors as errs_help


def get_config():
    # try:
    #     return json.loads(open('config.json', 'r').read())
    # except Exception:
    #     print("lflflfl")
    #     return {
    #         "database.config": {
    #             "user": "postgres",
    #             "password": "postgres",
    #             "host": "localhost",
    #             "database": "mydb2"
    #         }
    #     }

    return {
        "database.config": {
            "user": "postgres",
            "password": "postgres",
            "host": "localhost",
            "database": "mydb3"
        }
    }