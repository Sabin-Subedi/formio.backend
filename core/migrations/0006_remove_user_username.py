# Generated by Django 4.1.3 on 2022-11-24 15:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_user_github_oauth'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='username',
        ),
    ]
