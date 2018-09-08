from datetime import datetime

import croniter

import tracker_lib.helpers.errors as errs

"""Try to input period in cron format like
           ┌───────────── minute (0 - 59)
#          │ ┌───────────── hour (0 - 23)
#          │ │ ┌───────────── day of month (1 - 31)
#          │ │ │ ┌───────────── month (1 - 12)
#          │ │ │ │ ┌───────────── day of week (0 - 6) (Sunday to Saturday;
#          │ │ │ │ │                                       7 is also Sunday on some systems)
#          │ │ │ │ │
#          │ │ │ │ │
#          * * * * *  command to execute"""


class CronPeriodHelper:

    def is_valid_cron(period: str):
        try:
            croniter.croniter(period, datetime.now())
            check = True
        except Exception:
            check = False
        return check

    def get_tasks_periods(self, start_date, end_date, input_string='* * * * *'):
        """

        Returns all dates of periodic tasks from start date to end by cron parameter.

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
        itr = croniter.croniter(period, date.timestamp()-1)
        return itr.get_next(datetime).timestamp() == date.timestamp()
