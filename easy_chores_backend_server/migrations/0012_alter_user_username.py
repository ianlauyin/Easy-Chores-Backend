# Generated by Django 5.0.4 on 2024-05-17 15:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('easy_chores_backend_server', '0011_user_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=50),
        ),
    ]
