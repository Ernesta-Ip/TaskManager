# Generated by Django 5.2.1 on 2025-05-22 20:43

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0003_rename_assigned_users_card_members_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='board',
            name='members',
            field=models.ManyToManyField(blank=True, related_name='tasks_boards', to=settings.AUTH_USER_MODEL),
        ),
    ]
