# Generated by Django 5.0 on 2023-12-06 18:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0004_tasksmodel_about'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tasksmodel',
            name='about',
            field=models.TextField(blank=True, default=''),
        ),
    ]
