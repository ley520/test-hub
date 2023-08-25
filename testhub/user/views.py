from django.http import HttpRequest
from django.core.handlers.wsgi import WSGIRequest

# Create your views here.
from ninja.security import HttpBasicAuth
from ninja import NinjaAPI

import jwt

router = NinjaAPI()


class MyHttpBasicAuth(HttpBasicAuth):
    def authenticate(self, request: HttpRequest, username: str, password: str):
        pass


@router.get("/test")
def test_login(request: WSGIRequest):
    print(request)
    print(type(request))
    print(request.headers)
    print(request.user)
    print(request.META)
    return "success"
