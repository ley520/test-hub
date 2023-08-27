from ninja import NinjaAPI

from testhub.common.models import ProjectModel
from testhub.testcase.schemas import ProjectSchemaIn

router = NinjaAPI(title="测试用例管理", urls_namespace='testcases')


@router.get("/tree/{node_id}", description="获取某个节点下所有的节点")
def get_testcase_tree_node(request, node_id: int):
    return {}


@router.post("/tree/add/{node_id}", description="在某个节点下添加子节点")
def add_tree_node(request, node_id: int):
    return {}


@router.post("/project", description="新增项目")
def add_project(request, project_info: ProjectSchemaIn):
    project_info = project_info.dict()
    project_instance = ProjectModel.objects.create(**project_info)
    return {
        "msg": "创建成功",
        "data": {
            "project_id": project_instance.id,
            "project_name": project_instance.name,
            "project_desc": project_instance.desc
        }
    }


@router.delete("/project/{project_id}", description="删除项目")
def add_project(request, project_id: int):
    try:
        project = ProjectModel.objects.get(id=project_id, is_del=False)
        project.is_del = True
        project.save()
        return {
            "msg": "项目删除成功"
        }
    except ProjectModel.DoesNotExist:
        return {
            "msg": "项目不存在"
        }


@router.put("/project/{project_id}", description="更新项目")
def update_project(request, project_id: int, project_info: ProjectSchemaIn):
    project_info = project_info.dict()
    try:
        project_instance = ProjectModel.objects.get(id=project_id)
        for key, value in project_info.items():
            setattr(project_instance, key, value)
        project_instance.save()
        return {
            "msg": "成功",
            "data": {
                "project_id": project_instance.id,
                "project_name": project_instance.name,
                "project_desc": project_instance.desc
            }
        }
    except ProjectModel.DoesNotExist:
        return {
            "msg": "项目不存在"
        }


@router.get("/project", description="查询项目列表")
def query_project_list(request):
    project_list = ProjectModel.objects.filter(is_del=False)
    project_query_list = [{"project_id": project.id, "project_name": project.name, "project_desc": project.desc} for project in project_list]
    return {
        "msg": "成功",
        "data": project_query_list
    }


@router.get("/project/{project_id}", description="查询项目列表")
def query_project_list(request, project_id: int):
    try:
        project = ProjectModel.objects.get(is_del=False, id=project_id)
        return {
            "msg": "成功",
            "data": {
                "project_id": project.id,
                "project_name": project.name,
                "project_desc": project.desc,
            }
        }
    except ProjectModel.DoesNotExist:
        return {"msg": "成功", "data": None}
