# Generated by Django 3.2.7 on 2021-09-09 04:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0008_auto_20210909_0433'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mtexperiment',
            name='experiment_instance',
        ),
        migrations.AddField(
            model_name='mtexperiment',
            name='experiment_instances',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='experiment', to='common.experimentinstance'),
        ),
    ]
