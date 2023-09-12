# coding=utf-8
# data：2023/8/16-21:06
from .base import *

DEBUG = True
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "test-hub",
        "USER": "root",
        "PASSWORD": "123456",
        "HOST": "127.0.0.1",
        "PORT": "33006",
    }
}

