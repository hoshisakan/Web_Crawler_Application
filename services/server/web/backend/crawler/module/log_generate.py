from loguru import logger
from pathlib import Path
from module.date import DateTimeTools as DT


log_path = Path(Path.cwd(), "logs")

class Loggings():
    __instance = None
    logger.add(f"{log_path}//{DT.get_date(split_character='_')}.log", rotation="500MB", encoding="utf-8", enqueue=True,retention="1 days")
    
    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super(Loggings, cls).__new__(cls, *args, **kwargs)
        return cls.__instance

    def info(self, msg):
        return logger.info(msg)

    def debug(self, msg):
        return logger.debug(msg)

    def warning(self, msg):
        return logger.warning(msg)

    def error(self, msg):
        return logger.error(msg)