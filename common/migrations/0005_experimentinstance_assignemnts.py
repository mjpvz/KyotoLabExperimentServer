# Generated by Django 3.2.7 on 2021-09-09 06:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0004_auto_20210909_0515'),
    ]

    operations = [
        migrations.AddField(
            model_name='experimentinstance',
            name='assignemnts',
            field=models.IntegerField(default=1),
        ),
    ]
