# Generated by Django 5.1.2 on 2024-12-03 11:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hostEmployer', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tour',
            name='is_taken',
            field=models.BooleanField(default=False),
        ),
    ]
