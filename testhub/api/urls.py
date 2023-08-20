# coding=utf-8
# data：2023/8/18-13:18

from django.urls import path
from .views import api

urlpatterns = [
    path("api/", api.urls),
]
