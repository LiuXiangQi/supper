# Generated by Django 2.0.2 on 2019-09-21 06:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webkeyword', '0003_auto_20190921_1429'),
    ]

    operations = [
        migrations.RenameField(
            model_name='casegroup',
            old_name='CreateTime',
            new_name='createTime',
        ),
        migrations.RenameField(
            model_name='casegroup',
            old_name='GroupName',
            new_name='groupName',
        ),
        migrations.RenameField(
            model_name='casegroup',
            old_name='ProjectId',
            new_name='projectId',
        ),
        migrations.RenameField(
            model_name='casegroup',
            old_name='UpdateTime',
            new_name='updateTime',
        ),
        migrations.AddField(
            model_name='casegroup',
            name='description',
            field=models.CharField(blank=True, max_length=1024, null=True, verbose_name='描述'),
        ),
    ]
