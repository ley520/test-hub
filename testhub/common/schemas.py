#!/usr/bin/env python
# @Project: test-hub
# @Author: zero
# @Create time: 2023/8/27 11:17
from ninja import Schema, ModelSchema
from testhub.common.models import ProjectModel
from testhub.utils.BaseResponse import BaseRespSchema


class ProjectCreateSchema(Schema):
    name: str
    desc: str = None


class ProjectSchemaOut(BaseRespSchema):
    class Config:
        model = ProjectModel
        model_exclude = ['name', 'desc', 'testcase_root_tree_id']
