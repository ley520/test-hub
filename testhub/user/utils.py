# coding=utf-8
# data：2023/8/25-11:18
import jwt
import datetime

from django.http import HttpRequest
from jwt import exceptions
from ninja.security import HttpBearer

from config.settings.jwt import JWT_SECRET, JWT_EXPIRATION_DELTA_SECONDS, JWT_AUTH_HEADER, JWT_AUTH_HEADER_PREFIX
from django.conf import settings

from config import logger


def create_token(payload: dict):
    """
    :param payload:  例如：{'user_id':1,'username':'wupeiqi'}用户信息
    :param timeout: token的过期时间，默认20分钟
    :return:
    """
    headers = {
        'typ': 'jwt',
        'alg': 'HS256'
    }
    payload['exp'] = datetime.datetime.utcnow() + datetime.timedelta(seconds=JWT_EXPIRATION_DELTA_SECONDS)
    result = jwt.encode(payload=payload, key=JWT_SECRET, algorithm="HS256", headers=headers)
    return result


def parse_payload(token):
    """
    对token进行和发行校验并获取payload
    :param token:
    :return:
    """
    result = {'status': False, 'data': None, 'error': None}
    try:
        verified_payload = jwt.decode(token, JWT_SECRET, algorithms="HS256")
        result['status'] = True
        result['data'] = verified_payload
    except exceptions.ExpiredSignatureError:
        result['error'] = 'token已失效'
    except jwt.DecodeError:
        result['error'] = 'token认证失败'
    except jwt.InvalidTokenError:
        result['error'] = '非法的token'
    return result


class MyHttpBearer(HttpBearer):
    openapi_scheme: str = JWT_AUTH_HEADER_PREFIX
    header: str = JWT_AUTH_HEADER

    def authenticate(self, request, token):
        result = parse_payload(token)
        if result['status']:
            request.user = result['data']
            return request.user
        return False
