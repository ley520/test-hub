from typing import List

from ninja import Router, Query
from ninja.pagination import paginate

from testhub.common.schemas import ProjectCreateSchema, ProjectSchemaOut, ProjectFilterSchema, RequirementSchemaIn, RequirementSchemaOut, \
    RequirementFilterSchema, RequirementProjectSchemaOut
from .services import get_all_node, create_new_project, get_all_project, delete_project, update_project_info, get_project_detail, create_requirement, \
    update_requirement_info, delete_requirement, query_requirement_detail, query_requirement_list

from ..utils.BasePagination import CustomPagination
from ..utils.BaseResponse import BaseRespSchema
from ..utils.BaseStatusCode import CommonStatusCode

# Create your views here.
router = Router()


@router.get("/tree/{node_id}", description="获取某个节点下所有的节点")
def get_testcase_tree_node(request, node_id: int):
    node = get_all_node(node_id)
    return {}


@router.post("/tree/add/{node_id}", description="在某个节点下添加子节点")
def add_tree_node(request, node_id: int):
    return {}


@router.post("/project", description="添加项目", response=BaseRespSchema[ProjectSchemaOut])
def add_project(request, project_info: ProjectCreateSchema):
    project = create_new_project(project_info)
    return BaseRespSchema.build_success_resp(data=project)


@router.delete("/project/{project_id}", description="删除项目", response=BaseRespSchema)
def del_project(request, project_id: int):
    is_deleted = delete_project(project_id=project_id)
    if is_deleted:
        return BaseRespSchema.build_success_resp()
    else:
        return BaseRespSchema.build_fall_resp(code=CommonStatusCode.PROJECT_NOT_EXIST.code, message=CommonStatusCode.PROJECT_NOT_EXIST.msg)


@router.put("/project/{project_id}", description="更新项目", response=BaseRespSchema[ProjectSchemaOut])
def update_project(request, project_id: int, project_info: ProjectCreateSchema):
    project = update_project_info(project_id=project_id, project_info=project_info)
    if not project:
        return BaseRespSchema.build_fall_resp(code=CommonStatusCode.PROJECT_NOT_EXIST.code, message=CommonStatusCode.PROJECT_NOT_EXIST.msg)
    else:
        return BaseRespSchema.build_success_resp(data=project)


@router.get("/project", description="查询项目列表", response=List[ProjectSchemaOut])
@paginate(CustomPagination)
def query_project_list(request, filters: ProjectFilterSchema = Query(...)):
    projects = get_all_project(filters=filters)
    return projects


@router.get("/project/{project_id}", description="查询项目详情", response=BaseRespSchema[ProjectSchemaOut])
def query_project_detail(request, project_id: int):
    project = get_project_detail(project_id=project_id)
    return BaseRespSchema.build_success_resp(data=project)


@router.post('/requirements/add', description='添加需求', response=BaseRespSchema[RequirementSchemaOut])
def add_requirement(request, requirement_info: RequirementSchemaIn):
    user_id = request.user.id
    requirement = create_requirement(requirement_info=requirement_info, user_id=user_id)
    if not requirement:
        return BaseRespSchema.build_fall_resp(CommonStatusCode.PROJECT_NOT_EXIST.code, message=CommonStatusCode.PROJECT_NOT_EXIST.msg)
    return BaseRespSchema.build_success_resp(data=requirement)


@router.put('/requirement/{requirement_id}', description='更新需求信息', response=BaseRespSchema[RequirementSchemaOut])
def update_requirement(request, requirement_info: RequirementSchemaIn, requirement_id: int):
    user_id = request.user.id
    requirement = update_requirement_info(requirement_info=requirement_info, user_id=user_id, requirement_id=requirement_id)
    if not requirement:
        return BaseRespSchema.build_fall_resp(code=CommonStatusCode.REQUIREMENT_NOT_EXIST.code, message=CommonStatusCode.REQUIREMENT_NOT_EXIST.msg)
    return BaseRespSchema.build_success_resp(data=requirement)


@router.delete('/requirement/{requirement_id}', description='删除需求', response=BaseRespSchema)
def del_requirement(request, requirement_id: int):
    is_delete = delete_requirement(requirement_id=requirement_id)
    if not is_delete:
        return BaseRespSchema.build_fall_resp(CommonStatusCode.REQUIREMENT_NOT_EXIST.code, message=CommonStatusCode.REQUIREMENT_NOT_EXIST.msg)
    else:
        return BaseRespSchema.build_success_resp()


@router.get('/requirement/{requirement_id}', description='查询需求详情', response=BaseRespSchema[RequirementSchemaOut])
def get_requirement_detial(request, requirement_id: int):
    requirement = query_requirement_detail(requirement_id=requirement_id)
    if not requirement:
        return BaseRespSchema.build_fall_resp(CommonStatusCode.REQUIREMENT_NOT_EXIST.code, message=CommonStatusCode.REQUIREMENT_NOT_EXIST.msg)
    else:
        return BaseRespSchema.build_success_resp(data=requirement)


@router.get('/requirement/', description='查询需求列表', response=List[RequirementProjectSchemaOut])
@paginate(CustomPagination)
def get_requirement_list(request, filters: RequirementFilterSchema = Query(...)):
    requirement_combined_project_data = query_requirement_list(filters=filters)
    return requirement_combined_project_data
