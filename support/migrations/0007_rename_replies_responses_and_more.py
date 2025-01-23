# Generated by Django 5.1.2 on 2025-01-12 17:34

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('support', '0006_replies'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameModel(
            old_name='replies',
            new_name='responses',
        ),
        migrations.RenameField(
            model_name='responses',
            old_name='reply',
            new_name='response',
        ),
    ]