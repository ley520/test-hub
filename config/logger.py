# coding=utf-8
# data：2023/8/25-19:32

from loguru import logger as log
from datetime import datetime, timedelta, time
from django.conf import settings

import sys

# 去除默认控制台输出
log.remove()
# 输出日志格式
logger_format = "{time:YYYY-MM-DD HH:mm:ss,SSS} [{process}] {level} {file} {module} {function} {line} - {message}"

# 控制台输出
log.add(sys.stderr)


class Rotator:

    def __init__(self, size, at):
        self._size = size
        now = datetime.now()
        today_at_time = now.replace(hour=at.hour, minute=at.minute, second=at.second)
        if now >= today_at_time:
            # the current time is already past the target time so it would rotate already
            # add one day to prevent an immediate rotation
            self._next_rotate = today_at_time + timedelta(days=1)
        else:
            self._next_rotate = today_at_time

    def should_rotate(self, message, file):
        file.seek(0, 2)
        if file.tell() + len(message) > self._size:
            return True
        if message.record["time"].timestamp() > self._next_rotate.timestamp():
            self._next_rotate += timedelta(days=1)
            return True
        return False


rotator = Rotator(500 * 1024 * 1024, time(0, 0, 0))


def only_level(level):
    def is_level(record):
        return record["level"].name == level

    return is_level


config_map = {
    "format": logger_format,
    "rotation": rotator.should_rotate,
    "encoding": "utf-8",
    "enqueue": True,
    "retention": "30 days",
    "serialize": False,
    "compression": "zip",
}

log.add(str(settings.BASE_DIR) + "/log/info.{time:YYYY-MM-DD}.log",
        # format="{time:YYYY-MM-DD HH:mm:ss.SSS}-{level}-{message}",
        level="INFO",
        filter=only_level("INFO"),
        **config_map)

log.add(str(settings.BASE_DIR) + "/log/error.{time:YYYY-MM-DD}.log",
        level="ERROR",
        filter=only_level("ERROR"),
        backtrace=True,
        diagnose=True,
        **config_map)
log.add(str(settings.BASE_DIR) + "/log/debug.{time:YYYY-MM-DD}.log",
        level="DEBUG",
        filter=only_level("DEBUG"),
        backtrace=True,
        diagnose=True,
        **config_map)
logger = log
