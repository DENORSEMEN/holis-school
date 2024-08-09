# Generated by Django 5.0.7 on 2024-08-08 13:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authusers', '0005_alter_authuser_user_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='authuser',
            name='is_verified',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='authuser',
            name='otp',
            field=models.CharField(blank=True, max_length=6, null=True),
        ),
    ]
