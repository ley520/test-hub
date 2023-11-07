# coding=utf-8
# data：2023/8/18-13:18

# from ninja import NinjaAPI
# from testhub.user.views import router as user_router
# from testhub.testcase.views import router as testcase_router

from django.urls import path, include

# api = NinjaAPI()
#
# api.add_router("user", user_router)
# api.add_router("testcase", testcase_router)

urlpatterns = [
    path("common/", include("testhub.common.urls")),
]
