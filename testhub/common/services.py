# coding=utf-8
# data：2023/8/27-12:49
from django.db.models import QuerySet

from .models import TreeNode, ProjectModel
from config import logger
from .schemas import ProjectCreateSchema


# 查询
def get_all_node(node_id):
    tree = TreeNode.objects.filter(id=node_id)
    if tree:
        return tree[0].dump_bulk()
    return []


def create_root_tree_node(node_name) -> TreeNode:
    return TreeNode.add_root(name=node_name)


def create_child_tree_node(parent_node_id, name):
    parent_node = TreeNode.objects.filter(id=parent_node_id)
    if parent_node:
        child_node = parent_node[0].add_child(name=name)
        return child_node
    logger.info(f"父节点ID：{parent_node_id} 不存在")
    return False


def create_new_project(project_info: ProjectCreateSchema) -> ProjectModel:
    root_node = create_root_tree_node(project_info.name)
    project = project_info.dict().update({"testcase_root_tree_id": root_node.id})
    project_instance = ProjectModel.objects.create(project)
    return project_instance
