from django.db import models
from treebeard.mp_tree import MP_Node


class BaseModel(models.Model):
    create_time = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
    update_time = models.DateTimeField(verbose_name="更新时间", auto_now=True)
    is_del = models.BooleanField(default=False, blank=False, null=False, verbose_name="是否删除")

    class Meta:
        abstract = True


class Project(BaseModel):
    name = models.CharField(max_length=256, null=False, blank=False, verbose_name="项目名称")
    desc = models.TextField(verbose_name="项目描述和内容")

    def __str__(self):
        return self.name

    class Meta:
        db_table = "common_project"


class Requirement(BaseModel):
    name = models.CharField(max_length=256, null=False, blank=False, verbose_name="需求名称")
    desc = models.TextField(verbose_name="需求描述和内容")
    project = models.ForeignKey(
        Project, db_index=True, null=False, blank=False, db_constraint=False, on_delete=models.DO_NOTHING, verbose_name="所属项目"
    )

    def __str__(self):
        return self.name

    class Meta:
        db_table = "common_requirement"


class Directory(MP_Node, BaseModel):
    name = models.CharField(max_length=32, verbose_name="目录名称")
    project = models.ForeignKey(
        Project, null=True, blank=True, on_delete=models.CASCADE, related_name="directory", db_constraint=False, verbose_name="所属项目"
    )

    node_order_by = ["name"]

    def __str__(self):
        return self.name

    class Meta:
        unique_together = (("project", "name"),)
        db_table = "common_directory"
