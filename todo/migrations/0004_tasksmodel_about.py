# Generated by Django 5.0 on 2023-12-06 18:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0003_rename_tasks_tasksmodel'),
    ]

    operations = [
        migrations.AddField(
            model_name='tasksmodel',
            name='about',
            field=models.TextField(blank=True, null=True),
        ),
    ]
