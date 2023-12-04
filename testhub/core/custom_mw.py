#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created on: 2023/11/12
# Author: bitzero
import json
from time import time

from django.utils.deprecation import MiddlewareMixin
from testhub.utils.logger import logger


class LoggingMiddleware(MiddlewareMixin):
    """
    记录请求日志
    """

    def __call__(self, request):
        now = time()
        request_body = {}
        request_params = {}
        method = request.method
        request_path = request.build_absolute_uri()

        if request.method == "POST":
            if request.content_type == "application/json":
                request_body = json.loads(request.body)
            else:
                request_body = request.POST.dict()
        elif request.method == "GET":
            request_params = request.GET.dict()

        total = time() - now

        response = self.get_response(request)
        status_code = response.status_code
        logger.info(f"{method} {request_path} 请求参数: {request_params} 请求体: {request_body} 状态码: {status_code} 耗时: {total:.2f} 秒")
        return response
