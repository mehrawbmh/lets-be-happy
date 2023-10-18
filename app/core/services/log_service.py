import logging

from app.configs.settings import settings
from app.core.enum.env_modes import EnvMode
from app.core.enum.log_sections import LogSection
from app.core.services.service import Service


class LogService(Service):
    logger_name: LogSection = LogSection.DEFAULT
    log_string_format = "** %(levelname)s: ** %(message)s  ---  at %(asctime)s on %(name)s"

    class CustomFormatter(logging.Formatter):
        grey = '\x1b[38;21m'
        blue = '\x1b[38;5;39m'
        yellow = '\x1b[38;5;226m'
        red = '\x1b[38;5;196m'
        bold_red = '\x1b[31;1m'
        reset = '\x1b[0m'

        def __init__(self, fmt):
            super().__init__()
            self.fmt = fmt
            self.FORMATS = {
                logging.DEBUG: self.grey + self.fmt + self.reset,
                logging.INFO: self.blue + self.fmt + self.reset,
                logging.WARNING: self.yellow + self.fmt + self.reset,
                logging.ERROR: self.red + self.fmt + self.reset,
                logging.CRITICAL: self.bold_red + self.fmt + self.reset
            }

        def format(self, record):
            log_format = self.FORMATS.get(record.levelno)
            formatter = logging.Formatter(log_format)
            return formatter.format(record)

    def __init__(self):
        self.__logger = logging.getLogger(self.logger_name)
        self.__config()

    def __add_file_handler(self):
        file_handler = logging.FileHandler('app.log')
        file_handler.setFormatter(logging.Formatter(self.log_string_format))
        self.__logger.addHandler(file_handler)

    def __add_stdout_handler(self):
        colorful_handler = logging.StreamHandler()
        colorful_handler.setFormatter(self.CustomFormatter(self.log_string_format))
        self.logger.addHandler(colorful_handler)

    def __config(self):
        match settings.MODE:
            case EnvMode.PRODUCTION:
                self.__add_file_handler()
                self.__add_stdout_handler()
                level = logging.INFO
            case EnvMode.TEST:
                self.__add_stdout_handler()
                level = logging.DEBUG
            case _:
                level = logging.NOTSET

        self.__logger.setLevel(level)

    def set_logger(self, logger: logging.Logger):
        self.__logger = logger

    @property
    def logger(self) -> logging.Logger:
        return self.__logger

    def get_logger(self, name: str | None = None) -> logging.Logger:
        if name:
            self.__logger.name = name  # todo: the problem is you change the name for whole class
        return self.__logger


logService = LogService()
