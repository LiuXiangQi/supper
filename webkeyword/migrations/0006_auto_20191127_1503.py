# Generated by Django 2.2.1 on 2019-11-27 07:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webkeyword', '0005_auto_20190930_1309'),
    ]

    operations = [
        migrations.RenameField(
            model_name='case',
            old_name='case_name',
            new_name='caseName',
        ),
        migrations.RemoveField(
            model_name='case',
            name='browser_type',
        ),
        migrations.RemoveField(
            model_name='casegroup',
            name='user_id',
        ),
    ]
