#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created on: 2023/12/1
# Author: bitzero


from enum import Enum


class SystemStatusCode(Enum):
    SUCCESS = (0, "成功")
    ERROR = (-1, "失败")
    UNKNOWN_EXCEPTION = (9999, "未知异常，请联系管理员")

    @property
    def code(self):
        return self.value[0]

    @property
    def msg(self):
        return self.value[1]
