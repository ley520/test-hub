# coding=utf-8
# data：2023/8/25-19:32

from loguru import logger as log
from datetime import datetime, timedelta, time




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


rotator = Rotator(10000, time(0, 0, 0))
log.add("file.log", rotation=rotator.should_rotate)

log.add("info_{YYYY-MM-DD}.log", format="{time}-{level}-{message}", level="info", enqueue=True,
        rotation=rotator.should_rotate)

log.add("error_{YYYY-MM-DD}.log", format="{time}-{level}-{message}", level="error", enqueue=True, backtrace=True,
        diagnose=True)
logger = log
