# Generated by Django 5.1.2 on 2025-01-13 07:40

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('support', '0007_rename_replies_responses_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameModel(
            old_name='responses',
            new_name='Response',
        ),
        migrations.RenameField(
            model_name='response',
            old_name='response',
            new_name='responseId',
        ),
    ]
