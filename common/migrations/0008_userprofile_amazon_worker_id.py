# Generated by Django 3.2.7 on 2021-09-09 08:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0007_auto_20210909_0801'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='amazon_worker_id',
            field=models.CharField(blank=True, max_length=127, unique=True),
        ),
    ]
