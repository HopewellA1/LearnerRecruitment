# Generated by Django 4.2.3 on 2024-08-08 06:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('applicants', '0008_alter_learner_dob_alter_learner_equitycode_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='learner',
            name='DOB',
            field=models.DateField(blank=True, null=True),
        ),
    ]
