# Generated by Django 4.2.3 on 2024-08-04 12:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('applicants', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='Address',
            field=models.CharField(default='None', max_length=100),
        ),
    ]
