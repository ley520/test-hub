# Generated by Django 4.2.4 on 2023-08-30 13:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0002_remove_treenode_project_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='requirementmodel',
            name='create_user_id',
            field=models.PositiveIntegerField(null=True, verbose_name='创建人id'),
        ),
        migrations.AlterField(
            model_name='requirementmodel',
            name='update_user_id',
            field=models.PositiveIntegerField(null=True, verbose_name='修改人id'),
        ),
        migrations.AlterField(
            model_name='treenode',
            name='update_time',
            field=models.DateTimeField(auto_now=True, verbose_name='更 pl新时间'),
        ),
    ]
