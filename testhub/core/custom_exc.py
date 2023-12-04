#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created on: 2023/12/1
# Author: bitzero
from rest_framework.views import exception_handler
from rest_framework.exceptions import ValidationError
from testhub.utils.logger import logger
from testhub.utils.constants import SystemStatusCode


def handle_validation_error(exc, response):
    """
    处理字段校验错误
    """
    if isinstance(response.data, dict):
        # 取错误信息中的一组数据返回
        error_data = list(dict(response.data).items())[0]
        # 该组数据的 key ，对应模型中的某个字段
        error_key = error_data[0]
        # 该组数据的 value ，有可能是多个错误校验提示信息，这里只取第一条
        error_value = error_data[1][0]
        response.data["message"] = f"{error_key}: {error_value}"
        for key in dict(response.data).keys():
            # 删除多余错误信息
            if key != "message":
                response.data.pop(key)
        response.data["code"] = SystemStatusCode.ERROR.code
        response.data["data"] = None
    elif isinstance(response.data, list):
        response.data = {"code": SystemStatusCode.ERROR.code, "message": response.data[0], "data": None}

    if "detail" in response.data:
        response.data = {"code": SystemStatusCode.ERROR.code, "message": response.data.get("detail"), "data": None}
    else:
        response.data = {"code": SystemStatusCode.ERROR.code, "message": str(response.data), "data": None}
    return response


def custom_exception_handler(exc, context):
    """
    自定义异常，需要在 settings.py 文件中进行全局配置
    1.在视图中的 APIView 中使用时,需要在验证数据的时候传入 raise_exception=True 说明需要使用自定义异常
    2.ModelViewSet 中非自定义 action 已经使用了 raise_exception=True,所以无需配置
    """
    response = exception_handler(exc, context)
    if response is not None:
        # 字段校验错误处理
        if isinstance(exc, ValidationError):
            response = handle_validation_error(exc, response)
        else:
            logger.debug(f"未知异常: {exc.__class__.__name__}")
            response.data = {
                "code": SystemStatusCode.UNKNOWN_EXCEPTION.code,
                "message": SystemStatusCode.UNKNOWN_EXCEPTION.msg,
                "data": None,
            }
    else:
        logger.debug(f"未知异常: {exc.__class__.__name__}")
        logger.exception(exc)
        response = {"code": SystemStatusCode.UNKNOWN_EXCEPTION.code, "message": SystemStatusCode.UNKNOWN_EXCEPTION.msg, "data": None}
    return response
