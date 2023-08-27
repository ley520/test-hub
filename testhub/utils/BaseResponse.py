# coding=utf-8
# data：2023/8/27-13:33
from ninja import Schema, ModelSchema
from ninja.orm.metaclass import ModelSchemaMetaclass
from pydantic import BaseModel

from typing import Optional, Union, List


class BaseRespSchema(Schema):
    code: int
    message: Optional[str]
    data: Union[BaseModel, Schema, ModelSchema, dict, List, None]

    @staticmethod
    def build_success_resp(code, message, data):
        return BaseRespSchema(code=code, message=message, data=data)

    @staticmethod
    def build_fall_resp(code, message, data):
        return BaseRespSchema(code=code, message=message, data=data)
