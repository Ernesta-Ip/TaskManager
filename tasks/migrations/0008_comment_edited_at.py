# Generated by Django 5.2.2 on 2025-06-23 08:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0007_board_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='edited_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
