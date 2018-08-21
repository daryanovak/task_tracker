from datetime import datetime
from datetime import date

class StorageHelper:
    def __init__(self, cursor=None):
        self._cursor = cursor

    @staticmethod
    def dict_factory(cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

    @staticmethod
    def parse_data_to_objects(data: list, object_class: type):
        objects = list()

        for data_item in data:
            objects.append(object_class(**data_item))

        return objects

    @staticmethod
    def datetime_to_str(date):
        if date:
            return date.strftime("%d/%m/%y %H:%M")
        else:
            return " "
