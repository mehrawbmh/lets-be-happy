from datetime import datetime, timedelta, date

from pytz import timezone


class TimeService(datetime):
    @staticmethod
    def get_now() -> datetime:
        return datetime.utcnow()

    @staticmethod
    def get_today() -> date:
        return date.today()

    @staticmethod
    def get_today_start() -> datetime:
        return datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)

    @staticmethod
    def get_today_end() -> datetime:
        return datetime.today().replace(hour=23, minute=59, second=59, microsecond=0)

    @staticmethod
    def change_utc_to_ir(other_zone_datetime: datetime):
        ir_delta = timedelta(hours=3, minutes=30)
        return other_zone_datetime + ir_delta

    @staticmethod
    def go_to_ir_timezone(any_time_zone_datetime: datetime):
        utc_timezone = timezone('UTC')
        ir_timezone = timezone('Asia/Tehran')

        utc_datetime = utc_timezone.localize(any_time_zone_datetime)
        ir_datetime = utc_datetime.astimezone(ir_timezone)

        return ir_datetime

    @staticmethod
    def format(date_object: date, str_format='%Y-%m-%d %H:%M:%S'):
        return date_object.strftime(str_format)

    @classmethod
    def get_now_formatted(cls, str_format: str = '%Y-%m-%d %H:%M:%S'):
        return cls.get_now().strftime(str_format)
