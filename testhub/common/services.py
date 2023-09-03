# coding=utf-8
# data：2023/8/27-12:49
from typing import List, Optional, Dict

from django.db.models import Q

from .models import TreeNode, ProjectModel, RequirementModel
from config import logger
from .schemas import ProjectCreateSchema, ProjectFilterSchema, RequirementSchemaIn, RequirementFilterSchema, RequirementSchemaOut, ProjectSchemaOut, \
    RequirementProjectSchemaOut


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
    project = project_info.dict()
    project.update({"testcase_root_tree_id": root_node.id})
    project_instance = ProjectModel.objects.create(**project)
    return project_instance


def get_all_project(filters: ProjectFilterSchema) -> List[ProjectModel]:
    projects = ProjectModel.objects.filter(is_del=False)
    projects = filters.filter(projects)
    return projects


def get_project_detail(project_id: int) -> Optional[ProjectModel]:
    project = ProjectModel.objects.filter(id=project_id, is_del=False)
    if not project:
        return None
    return project[0]


def delete_project(project_id: int) -> bool:
    project = ProjectModel.objects.filter(id=project_id, is_del=False)

    if not project:
        logger.info(f"项目ID：{project_id} 不存在")
        return False

    project[0].is_del = True
    project.save()
    return True


def update_project_info(project_id: int, project_info: ProjectCreateSchema) -> Optional[ProjectModel]:
    project_info = project_info.dict()
    project = ProjectModel.objects.filter(id=project_id, is_del=False)
    if not project:
        logger.info(f"项目ID：{project_id} 不存在")
        return None

    for key, value in project_info.items():
        setattr(project[0], key, value)
    project.save()
    return project


def query_requirement_detail(requirement_id: int) -> Optional[RequirementModel]:
    requirement = RequirementModel.objects.filter(id=requirement_id, is_del=False)
    if not requirement:
        logger.info(f'需求ID {requirement_id} 不存在')
        return None
    return requirement


def query_requirement_list(filters: RequirementFilterSchema) -> List[RequirementProjectSchemaOut]:
    project_name = filters.project_name
    requirements = RequirementModel.objects.all()
    if project_name:
        project_ids = ProjectModel.objects.filter(name__icontains=project_name).values_list('id', flat=True)
        requirements = requirements.filter(project_id__in=project_ids, is_del=False)

    combined_result = []
    for requirment in requirements:
        project = ProjectModel.objects.get(id=requirment.project_id, is_del=False)
        requirment_info = RequirementSchemaOut.from_orm(requirment).dict()
        requirment_info.pop('project_id', None)
        requirment_info['project'] = ProjectSchemaOut.from_orm(project).dict()
        combined_result.append(requirment_info)
    # todo 需要返回queryset，否则会出现分页异常
    return combined_result


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
        setattr(requirement, key, value)
    requirement.update_user_id = user_id
    requirement.save()

    return requirement


def delete_requirement(requirement_id: int) -> bool:
    requirement = query_requirement_detail(requirement_id=requirement_id)

    if not requirement:
        logger.info(f"项目ID：{requirement_id} 不存在")
        return False

    requirement[0].is_del = True
    requirement.save()
    return True
