#!/usr/bin/env python
# @Project: test-hub
# @Author: zero
# @Create time: 2023/8/27 11:17
from ninja import Schema, ModelSchema
from testhub.common.models import ProjectModel


class ProjectSchemaIn(Schema):
    name: str
    desc: str = None


class ProjectSchemaOut(ModelSchema):
    class Config:
        model = ProjectModel
        model_exclude = ['is_del']
