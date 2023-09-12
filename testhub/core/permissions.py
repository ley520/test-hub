# coding=utf-8
# data：2023/8/30-11:26
from enum import Enum


class PermissionEnum(Enum):
    MANAGE_USER = 1, "用户管理权限"
    MANAGE_PROJECT = 2, "项目管理权限"


print(PermissionEnum.MANAGE_USER.value)
print(PermissionEnum.MANAGE_PROJECT.name)
