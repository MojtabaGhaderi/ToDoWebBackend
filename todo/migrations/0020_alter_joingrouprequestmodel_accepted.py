# Generated by Django 5.0 on 2023-12-21 13:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0019_alter_friendrequestmodel_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='joingrouprequestmodel',
            name='accepted',
            field=models.BooleanField(default=False),
        ),
    ]