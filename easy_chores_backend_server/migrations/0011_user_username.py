# Generated by Django 5.0.4 on 2024-05-17 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('easy_chores_backend_server', '0010_alter_user_groups_alter_user_user_permissions'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='username',
            field=models.TextField(default='user'),
            preserve_default=False,
        ),
    ]
