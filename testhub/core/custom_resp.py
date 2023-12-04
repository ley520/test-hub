#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created on: 2023/12/1
# Author: bitzero


from rest_framework.response import Response
from rest_framework import serializers
from testhub.utils.logger import logger


class JsonResponse(Response):
    """
    自定义接口响应数据格式类
    1.在视图类中的 APIView 中使用该 JsonResponse 返回响应数据
    2.ModelViewSet、Mixin 下派生的 APIView 类、views.APIView 都需要自己重写并返回 JsonResponse 格式的数据

    ModelViewSet Mixin example:
    res = super().create(request, *args, **kwargs)
    return JsonResponse(data=res.data, msg='success', code=20000, status=status.HTTP_201_CREATED, headers=res.headers)
    """

    def __init__(self, data=None, code=None, msg=None, status=None, template_name=None, headers=None, exception=False, content_type=None):
        super().__init__(None, status=status)

        if isinstance(data, serializers.Serializer):
            msg = (
                "You passed a Serializer instance as data, but " "probably meant to pass serialized `.data` or " "`.error`. representation."
            )
            raise AssertionError(msg)
        logger.debug(f"响应数据: {data}")
        self.data = {"code": code, "message": msg, "data": data}
        self.template_name = template_name
        self.exception = exception
        self.content_type = content_type

        if headers:
            for name, value in headers.items():
                self[name] = value
