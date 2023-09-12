# coding=utf-8
# data：2023/8/29-20:40
from ninja import Schema


class LoginSchema(Schema):
    username: str
    password: str
class CreateUserSchema(Schema):
    username: str
    password: str
    first_name: str
