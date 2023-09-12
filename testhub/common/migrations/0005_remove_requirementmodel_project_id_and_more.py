# Generated by Django 4.2.4 on 2023-09-11 17:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0004_alter_requirementmodel_create_user_id_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='requirementmodel',
            name='project_id',
        ),
        migrations.AddField(
            model_name='requirementmodel',
            name='project',
            field=models.ForeignKey(db_constraint=False, default=1, on_delete=django.db.models.deletion.DO_NOTHING, related_name='requirement', to='common.projectmodel'),
            preserve_default=False,
        ),
    ]
