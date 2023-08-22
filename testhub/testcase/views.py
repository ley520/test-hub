from ninja import NinjaAPI

router = NinjaAPI(title="测试用例管理")


@router.get("/tree/{node_id}", description="获取某个节点下所有的节点")
def get_testcase_tree_node(request, node_id: int):
    return {}


@router.post("/tree/add/{node_id}", description="在某个节点下添加子节点")
def add_tree_node(request, node_id: int):
    return {}


@router.get("/project", description="查询项目列表")
def query_project_list(request):
    return {}


@router.post("/project/add", description="新增项目")
def add_project(request):
    return {}


@router.post("/project/del/{project_id}", description="删除项目")
def add_project(request, project_id: int):
    return {}

