#!/usr/bin/env python
# @Project: test-hub
# @Author: zero
# @Create time: 2023/8/27 11:17
from typing import Optional

from ninja import Schema, ModelSchema, FilterSchema, Field
from testhub.common.models import ProjectModel


class ProjectCreateSchema(Schema):
    name: str
    desc: Optional[str]


class ProjectSchemaOut(ModelSchema):
    class Config:
        model = ProjectModel
        model_exclude = ['is_del']


# noinspection PyAbstractClass
class ProjectFilterSchema(FilterSchema):
    name: Optional[str] = Field(q='name__icontains')
