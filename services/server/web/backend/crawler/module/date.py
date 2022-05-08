import time
import datetime
from datetime import datetime as dt
# import pytz, dateutil.parser
from dateutil.parser import parse


class DateTimeTools():
    @staticmethod
    def obtain_days_datetime(value):
        return datetime.timedelta(days=value)

    @staticmethod
    def obtain_hours_datetime(value):
        return datetime.timedelta(hours=value)

    @staticmethod
    def obtain_minutes_datetime(value):
        return datetime.timedelta(minutes=value)

    @staticmethod
    def obtain_seconds_datetime(value):
        return datetime.timedelta(seconds=value)

    @staticmethod
    def get_date(split_character='-'):
        return dt.now().strftime(f"%Y{split_character}%m{split_character}%d")

    @staticmethod
    def get_yesterday_date():
        #TODO 返回當前的日期
        return (dt.now().today() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")

    @staticmethod
    def get_datetime():
        return dt.now().strftime("%Y-%m-%d-%H:%M:%S")

    @staticmethod
    def get_current_datetime():
        return dt.now()

    @staticmethod
    def get_current_year():
        return dt.now().year

    @staticmethod
    def get_current_date():
        return time.strftime("%Y_%m_%d")

    @staticmethod
    def format_datetime_str(format_datetime):
        return format_datetime.strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def format_date_str(format_date):
        return format_date.strftime("%Y-%m-%d")

    @staticmethod
    def format_str_time(str_time):
        return dt.strptime(str_time, '%H/%M').strftime('%H:%M')

    # @staticmethod
    # def format_str_date(str_date):
    #     return dt.strptime(str_date, '%Y-%m-%d')

    @staticmethod
    def format_str_date(str_date):
        return parse(str_date)

    # @classmethod
    # def format_local_datetime_to_str(cls, format_datetime):
    #     # return cls.format_datetime_str(format_datetime + cls.obtain_hours_datetime(8))
    #     utctime = dateutil.parser.parse(cls.format_datetime_str(format_datetime + cls.obtain_hours_datetime(8)))
    #     return utctime.astimezone(pytz.timezone("Asia/Taipei"))

    @staticmethod
    def format_second_str(format_datetime):
        return format_datetime.strftime("%S")

    @staticmethod
    def convert_timestamp_to_datetime(timestamp):
        return dt.fromtimestamp(timestamp)


    @staticmethod
    def convert_string_to_datetime(str_date=None):
        return dt.fromisoformat(str_date)
    
    @staticmethod
    def convert_timestamp_to_datetime(timestamp):
        # return dt.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
        return dt.fromtimestamp(timestamp).strftime('%Y-%m-%d')

    @staticmethod
    def get_specific_date(days=1):
        return (dt.now().today() - datetime.timedelta(days=days)).strftime("%m-%d")
    
    @staticmethod
    def get_datetime_convert_to_timestamp(str_datetime):
        return dt.timestamp(dt.strptime(str_datetime, '%Y-%m-%d %H:%M:%S'))