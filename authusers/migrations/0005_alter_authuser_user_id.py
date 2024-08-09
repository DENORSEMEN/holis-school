# Generated by Django 5.0.7 on 2024-08-07 21:08

import authusers.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authusers', '0004_alter_authuser_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='authuser',
            name='user_id',
            field=models.CharField(default=authusers.models.generate_unique_user_id, max_length=6, unique=True),
        ),
    ]
