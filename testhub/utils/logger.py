# coding=utf-8
# data：2023/8/25-19:32

from loguru import logger as log
from datetime import datetime, timedelta, time
from django.conf import settings
import sys
import os

# 输出日志格式
LOGGER_FORMAT = (
    "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
    "<level>{level}</level> | "
    "<blue>{process.name}:{process.id}</blue> | "
    "<blue>{thread.name}</blue> | "
    "<blue>{name}:{function}:{line}</blue> "
    "<level> 👉 {message}</level>"
)

LOG_PATH = os.path.join(settings.BASE_DIR, "log")
os.makedirs(LOG_PATH, exist_ok=True)

# 去除默认控制台输出
log.remove()

log.level("DEBUG", color="<blue>")
log.level("INFO", color="<green>")
log.level("ERROR", color="<red>")

# 控制台输出
log.add(sys.stdout, level="DEBUG", format=LOGGER_FORMAT)


class Rotator:
    def __init__(self, size, at):
        self._size = size
        now = datetime.now()
        today_at_time = now.replace(hour=at.hour, minute=at.minute, second=at.second)
        self._next_rotate = today_at_time + timedelta(days=(1 if now >= today_at_time else 0))

    def should_rotate(self, message, file):
        file.seek(0, 2)
        if file.tell() + len(message) > self._size:
            return True
        if message.record["time"].timestamp() > self._next_rotate.timestamp():
            self._next_rotate += timedelta(days=1)
            return True
        return False


def only_level(level):
    def is_level(record):
        return record["level"].name == level

    return is_level


# 设置文件日志
def setup_file_logging(filename: str, level: str = "DEBUG", size: int = 500 * 1024 * 1024, at: time = time(0, 0, 0), **kwargs):
    """
    设置日志文件
    """
    log_file_path = os.path.join(LOG_PATH, filename)
    os.makedirs(os.path.dirname(log_file_path), exist_ok=True)

    rotator = Rotator(size=size, at=at)
    config_map = {
        "format": LOGGER_FORMAT,
        "rotation": rotator.should_rotate,
        "encoding": "utf-8",
        "enqueue": True,
        "retention": "30 days",
        "serialize": False,
        "compression": "zip",
    }
    if kwargs.get("filter"):
        kwargs["filter"] = only_level(kwargs["filter"])

    config_map.update(kwargs)

    log.add(log_file_path, level=level, **config_map)


setup_file_logging(
    filename="test-hub-info.log",
    level="DEBUG",
    filter="DEBUG",
    backtrace=True,
    diagnose=True,
)

setup_file_logging(
    filename="test-hub-error.log",
    level="ERROR",
    filter="ERROR",
    backtrace=True,
    diagnose=True,
)

logger = log
