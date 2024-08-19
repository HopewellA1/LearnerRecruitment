# Generated by Django 4.2.3 on 2024-08-08 09:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('applicants', '0011_alter_learner_nqflevel'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='code',
            field=models.CharField(default='None', max_length=15),
        ),
        migrations.AddField(
            model_name='category',
            name='description',
            field=models.CharField(default='N/A', max_length=500),
        ),
        migrations.AlterField(
            model_name='category',
            name='categoryName',
            field=models.CharField(max_length=100),
        ),
    ]