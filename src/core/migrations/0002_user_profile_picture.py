# Generated by Django 3.0.9 on 2020-08-27 15:08

import core.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='profile_picture',
            field=models.ImageField(null=True, upload_to=core.models.profile_picture_file_path),
        ),
    ]