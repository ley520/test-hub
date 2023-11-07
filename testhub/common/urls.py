#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created on: 2023/11/7
# Author: bitzero


from django.urls import path
from testhub.common.views import DirectoryAPI, DirectoryDetailAPI, ProjectAPI, ProjectDetailAPI, RequirementAPI, RequirementDetailAPI

urlpatterns = [
    path("directory/", DirectoryAPI.as_view(), name="directory"),
    path("directory/<int:pk>/", DirectoryDetailAPI.as_view(), name="directory-detail"),
    path("project/", ProjectAPI.as_view(), name="project"),
    path("project/<int:pk>/", ProjectDetailAPI.as_view(), name="project-detail"),
    path("requirement/", RequirementAPI.as_view(), name="requirement"),
    path("requirement/<int:pk>/", RequirementDetailAPI.as_view(), name="requirement-detail"),
]
