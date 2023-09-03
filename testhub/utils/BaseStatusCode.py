#!/usr/bin/env python
# @Project: test-hub
# @Author: zero
# @Create time: 2023/8/28 15:52

from enum import Enum


class CommonStatusCode(Enum):
    PROJECT_NOT_EXIST = (10001, '项目不存在')
    REQUIREMENT_NOT_EXIST = (10002, '需求不存在')

    @property
    def code(self):
        return self.value[0]

    @property
    def msg(self):
        return self.value[1]
