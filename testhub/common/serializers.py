#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created on: 2023/11/7
# Author: bitzero


from rest_framework import serializers

from testhub.common.models import Directory, Project, Requirement


class DirectorySerializer(serializers.ModelSerializer):
    parent = serializers.PrimaryKeyRelatedField(queryset=Directory.objects.all(), required=False, allow_null=True, write_only=True)
    children = serializers.SerializerMethodField()

    class Meta:
        model = Directory
        fields = ["id", "name", "project_id", "parent", "children", "depth"]
        read_only_fields = ["depth"]

    def get_children(self, obj):
        children = obj.get_children()
        if children:
            return self.__class__(children, many=True).data
        return []

    def create(self, validated_data):
        parent = validated_data.pop("parent", None)
        if parent is not None:
            directory = parent.add_child(**validated_data)
        else:
            directory = Directory.add_root(**validated_data)
        return directory

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.save()
        return instance


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ["id", "name", "desc", "create_time", "update_time"]
        read_only_fields = ["create_time", "update_time"]


class RequirementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Requirement
        fields = ["id", "name", "desc", "project_id", "create_time", "update_time"]
        read_only_fields = ["create_time", "update_time"]
