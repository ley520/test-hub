#!/usr/bin/env python
# @Project: test-hub
# @Author: zero
# @Create time: 2023/8/27 11:17
from datetime import datetime
from typing import Optional

from ninja import Schema, ModelSchema, FilterSchema, Field
from testhub.common.models import ProjectModel, RequirementModel


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


class RequirementSchemaIn(Schema):
    name: str
    desc: str
    project_id: int


class RequirementSchemaOut(ModelSchema):
    class Config:
        model = RequirementModel
        model_exclude = ['is_del']


# noinspection PyAbstractClass
class RequirementFilterSchema(FilterSchema):
    name: Optional[str] = Field(q='name__icontains')
    project_name: Optional[str]


class RequirementProjectSchemaOut(RequirementSchemaOut):
    project: ProjectSchemaOut
