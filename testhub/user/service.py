# coding=utf-8
# data：2023/8/29-20:37

from django.contrib.auth.models import User, Group
from django.contrib.auth.hashers import make_password, check_password
from django.conf import settings
from django.forms import model_to_dict
from django.http import HttpResponseForbidden

from testhub.common.models import ProjectModel
from testhub.user.schemas import CreateUserSchema, LoginSchema
from testhub.user.utils import create_token


def user_login(user: LoginSchema):
    user_instance_list = User.objects.filter(name=user.username)
    if user_instance_list and user_instance_list[0].check_password(user.password):
        return create_token(model_to_dict(user_instance_list[0], exclude=["password"]))

    else:
        raise HttpResponseForbidden


def add_group(request):
    pass


def add_user(request, user_info: CreateUserSchema):
    request_user: User = User.objects.get(id=request.user.id)
    # 只有超级管理员可以添加用户
    if request_user.is_superuser:
        user_info.password = make_password(password=user_info.password, salt=settings.USER_PASSWORD_SECRET_KEY)
        user_instance: User = User.objects.create_user(username=user_info.username, password=user_info.password)
        return user_instance
    else:
        raise HttpResponseForbidden

# Group.objects.create()
