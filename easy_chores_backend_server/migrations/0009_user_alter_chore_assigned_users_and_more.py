# Generated by Django 5.0.4 on 2024-05-17 15:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('easy_chores_backend_server', '0008_alter_chore_assigned_users_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('groups', models.ManyToManyField(blank=True, related_name='easy_chores_backend_server_user_set', to='auth.group')),
                ('user_permissions', models.ManyToManyField(blank=True, related_name='easy_chores_backend_server_user_set', to='auth.permission')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterField(
            model_name='chore',
            name='assigned_users',
            field=models.ManyToManyField(blank=True, related_name='chores', to='easy_chores_backend_server.user'),
        ),
        migrations.AlterField(
            model_name='grocery',
            name='creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='groceries', to='easy_chores_backend_server.user'),
        ),
    ]
