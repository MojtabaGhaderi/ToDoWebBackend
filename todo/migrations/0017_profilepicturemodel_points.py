# Generated by Django 5.0 on 2023-12-17 16:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0016_merge_20231217_1156'),
    ]

    operations = [
        migrations.AddField(
            model_name='profilepicturemodel',
            name='points',
            field=models.IntegerField(default=0, editable=False),
        ),
    ]
