# Generated by Django 5.1.2 on 2024-11-29 07:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('support', '0003_query_name_query_surname'),
    ]

    operations = [
        migrations.AddField(
            model_name='query',
            name='resolved',
            field=models.BooleanField(default=False),
        ),
    ]
