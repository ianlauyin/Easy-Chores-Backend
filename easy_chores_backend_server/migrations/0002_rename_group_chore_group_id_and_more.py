# Generated by Django 5.0.4 on 2024-05-08 08:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('easy_chores_backend_server', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='chore',
            old_name='group',
            new_name='group_id',
        ),
        migrations.RenameField(
            model_name='grocery',
            old_name='creator',
            new_name='creator_id',
        ),
        migrations.RenameField(
            model_name='grocery',
            old_name='group',
            new_name='group_id',
        ),
        migrations.RenameField(
            model_name='groceryphoto',
            old_name='grocery',
            new_name='grocery_id',
        ),
    ]
