from django.db import models
from treebeard.mp_tree import MP_Node


# Create your models here.

class BaseModel(models.Model):
    create_time = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
    update_time = models.DateTimeField(verbose_name="更新时间", auto_now=True)

    class Meta:
        abstract = True


class ProjectModel(BaseModel):
    """
    项目表
    """
    name = models.CharField(verbose_name="项目名称", max_length=256, null=False, blank=False)
    desc = models.TextField(verbose_name="项目描述和内容")
    testcase_root_tree_id = models.PositiveIntegerField(verbose_name="测试用例树的父id", null=True, blank=True)
    create_user_id = models.PositiveIntegerField(verbose_name="创建人", default=0)
    is_del = models.BooleanField(default=False, null=False, blank=False)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "project"
        permissions = (
            ('project_manager', 'manage project'),
            ('project_member', 'project team members'),
        )


class RequirementModel(BaseModel):
    """
    需求表
    """
    name = models.CharField(verbose_name="需求名称", max_length=256)
    desc = models.TextField(verbose_name="需求描述和内容")
    create_user_id = models.PositiveIntegerField(verbose_name="创建人id")
    update_user_id = models.PositiveIntegerField(verbose_name="修改人id", null=True)
    project = models.ForeignKey(to=ProjectModel, db_index=True, related_name='requirement', on_delete=models.DO_NOTHING, db_constraint=False)
    is_del = models.BooleanField(default=False, null=False, blank=False)

    class Meta:
        db_table = "requirement"


class TreeNode(MP_Node):
    """
    目录表
    """
    name = models.CharField(max_length=32)
    # project_id = models.PositiveIntegerField(null=True)
    create_time = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
    update_time = models.DateTimeField(verbose_name="更新时间", auto_now=True)
    node_order_by = ['name']

    def __str__(self):
        return self.name

    class Meta:
        db_table = "tree_node"
