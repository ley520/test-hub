from django.http import HttpRequest
from django.core.handlers.wsgi import WSGIRequest

# Create your views here.
from ninja.security import HttpBasicAuth
from ninja import NinjaAPI

from ninja import Schema

from .utils import create_token, parse_payload, htt_auth_with_token

router = NinjaAPI()


class MyHttpBasicAuth(HttpBasicAuth):
    def authenticate(self, request: HttpRequest, username: str, password: str):
        pass


@router.get("/test", auth=htt_auth_with_token)
def test_login(request: WSGIRequest):
    print(request)
    print(type(request))
    print(request.headers)
    print(request.user)
    print(request.META)
    return "success"


class LoginSchema(Schema):
    username: str
    password: str


@router.post("/login")
def login(request, user_info: LoginSchema):
    return create_token(user_info.dict())


@router.post("/check")
def login(request, token: str):
    return parse_payload(token)
