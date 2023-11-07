# coding=utf-8
# data：2023/8/27-12:49
from django.db.models import QuerySet
from treebeard.mp_tree import MP_NodeQuerySet


def get_tree_root(queryset: MP_NodeQuerySet) -> QuerySet:
    """
    获取结构树根
    :param queryset: MP_NodeQuerySet
    :return: 根节点
    """
    return queryset.filter(depth=1)


def get_node_by_id(queryset: MP_NodeQuerySet, node_id: int) -> QuerySet:
    """
    根据id获取节点
    :param queryset: MP_NodeQuerySet
    :param node_id: 节点id
    :render: 节点
    """
    return queryset.filter(id=node_id, depth=0).first()
