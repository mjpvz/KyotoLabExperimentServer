# Generated by Django 3.2.7 on 2021-09-09 04:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0002_auto_20210909_0442'),
    ]

    operations = [
        migrations.AddField(
            model_name='experimentinstance',
            name='condition',
            field=models.IntegerField(default=0),
        ),
    ]
