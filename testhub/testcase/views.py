from ninja import Router

router = Router()


@router.get("/list")
def get_testcase_list():
    pass


@router.get("/{project_id}/{testcase_id}")
def query_testcase_detail(project_id: int, testcase_id: int):
    pass
