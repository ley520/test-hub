# coding=utf-8
# data：2023/8/27-12:49
from typing import List, Optional
from django.contrib.auth.models import Group, User
from django.http import HttpResponseForbidden
from guardian.shortcuts import assign_perm
from testhub.common.models import (
    TreeNode,
    ProjectModel,
    RequirementModel
)
from config import logger
from testhub.common.schemas import (
    ProjectCreateSchema,
    ProjectFilterSchema,
    RequirementSchemaIn,
    RequirementFilterSchema, RequirementSchemaOut,
)


# 查询
# todo 解决树形结构问题
def get_all_node(node_id):
    tree = TreeNode.objects.filter(id=node_id)
    if tree:
        return tree.first().dump_bulk()
    return None


def create_root_tree_node(node_name) -> TreeNode:
    return TreeNode.add_root(name=node_name)


def create_child_tree_node(parent_node_id, name):
    parent_node = TreeNode.objects.filter(id=parent_node_id).first()
    if parent_node:
        child_node = parent_node.add_child(name=name)
        return child_node
    logger.info(f"父节点ID：{parent_node_id} 不存在")
    return False


def create_new_project(request, project_info: ProjectCreateSchema) -> ProjectModel:
    user: User = User.objects.filter(id=request.user["id"])
    if user:
        root_node = create_root_tree_node(project_info.name)
        project = project_info.dict()
        project.update({"testcase_root_tree_id": root_node.id})
        project_instance = ProjectModel.objects.create(**project)
        # 创建项目的权限分组：管理员组和用户组，并赋予权限
        group_manager = Group.objects.create(name=f"{project_info.name}_manager")
        group_member = Group.objects.create(name=f"{project_info.name}_member")
        assign_perm("common.project_manager", group_manager)
        assign_perm("common.project_member", group_member)
        user.groups.add(group_manager)
        return project_instance
    else:
        raise HttpResponseForbidden(content="请重新登录")


def get_all_project(filters: ProjectFilterSchema) -> List[ProjectModel]:
    projects = ProjectModel.objects.filter(is_del=False)
    projects = filters.filter(projects)
    return projects


def get_project_detail(project_id: int) -> Optional[ProjectModel]:
    project = ProjectModel.objects.filter(id=project_id, is_del=False).first()
    if not project:
        return None
    return project


def delete_project(project_id: int) -> bool:
    project = ProjectModel.objects.filter(id=project_id, is_del=False).first()

    if not project:
        logger.info(f"项目ID：{project_id} 不存在")
        return False

    project.is_del = True
    project.save()
    return True


def update_project_info(project_id: int, project_info: ProjectCreateSchema) -> Optional[ProjectModel]:
    project_info = project_info.dict()
    project = get_project_detail(project_id=project_id)

    if not project:
        logger.info(f"项目ID：{project_id} 不存在")
        return None

    for key, value in project_info.items():
        setattr(project, key, value)
    project.save()
    return project


def query_requirement_detail(requirement_id: int) -> Optional[RequirementModel]:
    requirement = RequirementModel.objects.select_related().filter(project__is_del=False, is_del=False, id=requirement_id).first()
    if not requirement:
        logger.info(f'需求ID {requirement_id} 不存在')
        return None
    return requirement


def query_requirement_list(filters: RequirementFilterSchema) -> List[RequirementSchemaOut]:
    project_name = filters.project_name
    requirements = RequirementModel.objects.select_related().filter(is_del=False, project__is_del=False)
    if project_name:
        requirements = RequirementModel.objects.select_related().filter(project__name__icontains=project_name, project__is_del=False, is_del=False)
    return requirements


def create_requirement(requirement_info: RequirementSchemaIn, user_id: int) -> Optional[RequirementModel]:
    requirement_payload = requirement_info.dict()
    project_id = requirement_payload['project_id']

    project = get_project_detail(project_id=project_id)
    if not project:
        logger.info(f'项目ID: {project_id} 不存在')
        return None

    requirement_payload.update({'create_user_id': user_id})
    requrement = RequirementModel(**requirement_payload)
    requrement.save()
    return requrement


def update_requirement_info(requirement_info: RequirementSchemaIn, user_id: int, requirement_id: int) -> Optional[RequirementModel]:
    requirement_payload = requirement_info.dict()

    project = get_project_detail(project_id=requirement_payload['project_id'])
    if not project:
        logger.info(f'项目ID: {requirement_id} 不存在')
        return None

    requirement = query_requirement_detail(requirement_id=requirement_id)

    for key, value in requirement_payload.items():
        if key == 'project_id' and value == requirement.project.id:
            continue
        setattr(requirement, key, value)
    requirement.update_user_id = user_id
    requirement.save()

    return requirement


def delete_requirement(requirement_id: int) -> bool:
    requirement = query_requirement_detail(requirement_id=requirement_id)
    if not requirement:
        logger.info(f"项目ID：{requirement_id} 不存在")
        return False

    requirement.is_del = True
    requirement.save()
    return True
