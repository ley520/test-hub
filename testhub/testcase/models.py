from django.db import models

from treebeard.mp_tree import MP_Node


class BaseModel(models.Model):
    create_time = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
    update_time = models.DateTimeField(verbose_name="更新时间", auto_now=True)

    class Meta:
        abstract = True


class TestcaseTypeEnum(models.IntegerChoices):
    FUNCTION_TEST = 1, "功能测试"
    AUTO_TEST = 2, "自动化测试"


class Testcase(BaseModel):
    """
    测试用例定义
    todo：属性不是最终属性，还需要补充
    """
    title = models.CharField(verbose_name="用例标题", max_length=256)
    desc = models.TextField(verbose_name="用例描述")
    pre_step = models.TextField(verbose_name="前置条件")
    step = models.TextField(verbose_name="用例步骤")
    type = models.PositiveIntegerField(verbose_name="Case类型", choices=TestcaseTypeEnum.choices,
                                       default=TestcaseTypeEnum.FUNCTION_TEST)
    version = models.PositiveIntegerField(verbose_name="用例版本", default=1)
    creator = models.PositiveIntegerField(verbose_name="创建者")
    updater = models.PositiveIntegerField(verbose_name="更。、新者")
    tree_node_id = models.PositiveIntegerField(verbose_name="所属节点ID")

    class Meta:
        db_table = "testcase"


class TestcaseSnapshot(Testcase):
    """
    测试用例快照
    """
    testcase_id = models.PositiveIntegerField(verbose_name="用例id", blank=False, null=False)

    class Meta:
        db_table = "testcase_snapshot"


class TestPlan(BaseModel):
    """
    测试计划，关联测试用例和需求
    可以单独存在也可以和需求绑定。
    """
    name = models.CharField(verbose_name="测试计划名称", max_length=32)
    user = models.PositiveIntegerField('')


class TestcaseRunStatusEnum(models.IntegerChoices):
    INIT = 1, "待执行"
    SUCCESS = 2, "通过"
    FAIL = 3, "失败"
    BLOCK = 4, "阻塞"


class PlanCaseMapping(BaseModel):
    test_plan_id = models.PositiveIntegerField()
    testcase_id = models.PositiveIntegerField()
    testcase_status = models.PositiveIntegerField(verbose_name="用例执行状态", choices=TestcaseRunStatusEnum.choices,
                                                  default=TestcaseRunStatusEnum.INIT)
    executor = models.PositiveIntegerField(verbose_name="执行人")
