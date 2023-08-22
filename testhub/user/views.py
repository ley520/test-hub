from django.http import HttpRequest
from django.shortcuts import render

# Create your views here.
from ninja.security import HttpBasicAuth
from ninja import NinjaAPI

import jwt

router = NinjaAPI()


class MyHttpBasicAuth(HttpBasicAuth):
    def authenticate(self, request: HttpRequest, username: str, password: str):
        pass


@router.get("/test")
def test_login(request):
    return "success"
