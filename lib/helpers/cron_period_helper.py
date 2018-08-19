import sqlite3
import croniter
from datetime import datetime, timedelta

"""* * * * * Команда, которая будет выполнена
   - - - - -
   | | | | | 
   | | | | - День недели (1 - 7) (воскресенье =  7)
   | | | --- Месяц (1 - 12)
   | | --- День месяца (1 - 31)
   | ---- Час (0 - 23)
   
   ----- Минута (0 - 59)"""


class CronPeriodHelper:
    def get_tasks_periods(self, start_date, end_date, input_string='* * * * *'):
        """
        Returns all dates of periodic tasks  from start date to end by cron parameter
        :param start_date: datetime
        :param end_date: datetime
        :param input_string: cron string "* * * * *"
        :return:sets of periodic dates
        """
        if input_string is str:
                raise errs.CronValueError()
        itr = croniter.croniter(input_string, start_date)
        next_date = itr.get_next(datetime)

        periods = set()
        while next_date <= end_date:
            periods.add(next_date.date().__str__())
            next_date = itr.get_next(datetime)

        return periods

    def in_period(self, period: str, date):
        """
        Checks availability of date in the cron period
        :param period: string (cron)
        :param date_timestamp: int (timestamp)
        :return: date in timestamp format
        """
        date = date if isinstance(date, datetime) else datetime.strptime(date, '%d/%m/%y')
        itr = croniter.croniter(period, date.timestamp())
        return itr.get_next(datetime).timestamp() == date.timestamp()

    """
     def get_tasks_period_by_date(date, input_string='* * * * 2'):
        itr = croniter.croniter(input_string, date)
        date_prev_iteration = itr.get_prev(datetime)
        now_date = datetime.now()
        while date_prev_iteration > now_date:
            date_prev_iteration = itr.get_prev(datetime)
            print(date_prev_iteration)

    def get_period(input_string, start_date, end_date):
        itr = croniter.croniter(input_string, start_date)
        date_next_iteration = itr.get_next(datetime)
        period_timestamp = (date_next_iteration.timestamp() - start_date.timestamp())
        return period_timestamp
    """

