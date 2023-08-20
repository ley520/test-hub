from django.db import models

from treebeard.mp_tree import MP_Node


class BaseModel(models.Model):
    create_time = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
    update_time = models.DateTimeField(verbose_name="更新时间", auto_now=True)

    class Meta:
        abstract = True


class ProjectModel(BaseModel):
    '''
    项目表
    '''
    name = models.CharField(verbose_name="项目名称", max_length=256, null=False, blank=False)
    desc = models.TextField(verbose_name="项目描述和内容")
    is_del = models.BooleanField(default=False, null=False, blank=False)

    class Meta:
        db_table = "project"


class RequirementModel(BaseModel):
    '''
    需求表
    '''
    name = models.CharField(verbose_name="需求名称", max_length=256)
    desc = models.TextField(verbose_name="需求描述和内容")
    project_id = models.PositiveIntegerField(db_index=True, null=False, blank=False)
    is_del = models.BooleanField(default=False, null=False, blank=False)

    class Meta:
        db_table = "requirement"


class TestcaseTreeNode(MP_Node):
    '''
    Case目录表，每个项目只可以创建1个总目录，但是子目录不做任何限制
    '''
    name = models.CharField(max_length=32)
    project_id = models.PositiveIntegerField(db_index=True, null=False, blank=False)
    create_time = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
    update_time = models.DateTimeField(verbose_name="更新时间", auto_now=True)
    node_order_by = ['name']

    def __str__(self):
        return self.name

    class Meta:
        db_table = "testcase_tree"
