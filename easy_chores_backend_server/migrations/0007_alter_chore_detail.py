# Generated by Django 5.0.4 on 2024-05-10 10:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('easy_chores_backend_server', '0006_alter_grocery_detail'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chore',
            name='detail',
            field=models.TextField(default='', max_length=500),
        ),
    ]
