class StorageHelper:
    def __init__(self, cursor=None):
        self._cursor = cursor

    @staticmethod
    def datetime_to_str(date):
        if date:
            return date.strftime("%d/%m/%y %H:%M")
        else:
            return " "
