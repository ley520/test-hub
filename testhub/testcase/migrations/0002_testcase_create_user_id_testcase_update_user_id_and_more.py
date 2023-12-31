# Generated by Django 4.2.4 on 2023-08-27 05:23

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("testcase", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="testcase",
            name="create_user_id",
            field=models.PositiveIntegerField(default=0, verbose_name="创建者"),
        ),
        migrations.AddField(
            model_name="testcase",
            name="update_user_id",
            field=models.PositiveIntegerField(default=0, verbose_name="更新者"),
        ),
        migrations.AddField(
            model_name="testplan",
            name="create_user_id",
            field=models.PositiveIntegerField(default=0, verbose_name="创建者"),
        ),
        migrations.AddField(
            model_name="testplan",
            name="update_user_id",
            field=models.PositiveIntegerField(default=0, verbose_name="更新者"),
        ),
        migrations.AlterField(
            model_name="testcase",
            name="tree_node_id",
            field=models.PositiveIntegerField(default=0, verbose_name="所属节点ID"),
        ),
        migrations.AddIndex(
            model_name="testcase",
            index=models.Index(fields=["tree_node_id"], name="tree_node_idx"),
        ),
    ]
