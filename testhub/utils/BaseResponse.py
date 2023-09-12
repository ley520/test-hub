# coding=utf-8
# data：2023/8/27-13:33
from ninja import Schema, ModelSchema
from pydantic import BaseModel

from typing import Optional, TypeVar, Generic
from pydantic import generics

T = TypeVar('T')


class BaseRespSchema(generics.GenericModel, Generic[T]):
    code: int
    message: str
    data: Optional[T]

    @classmethod
    def build_success_resp(cls, data=None):
        return cls(code=200, message='success', data=data)

    @classmethod
    def build_fall_resp(cls, code, message, data=None):
        return cls(code=code, message=message, data=data)
