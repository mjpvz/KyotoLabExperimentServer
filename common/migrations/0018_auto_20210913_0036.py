# Generated by Django 3.2.7 on 2021-09-13 00:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0017_alter_experimentinstance_reward'),
    ]

    operations = [
        migrations.AlterField(
            model_name='experimentinstance',
            name='keywords',
            field=models.CharField(blank=True, max_length=1000),
        ),
        migrations.AlterField(
            model_name='experimentinstance',
            name='reward',
            field=models.DecimalField(blank=True, decimal_places=4, max_digits=8, null=True),
        ),
        migrations.AlterField(
            model_name='experimentinstance',
            name='title',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
