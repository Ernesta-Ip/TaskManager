# Generated by Django 5.2.2 on 2025-06-12 15:36

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0005_board_user'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='board',
            name='user',
        ),
        migrations.AddField(
            model_name='board',
            name='created_by',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='boards_created', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
