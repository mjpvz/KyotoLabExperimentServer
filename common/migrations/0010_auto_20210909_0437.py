# Generated by Django 3.2.7 on 2021-09-09 04:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0009_auto_20210909_0436'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mtexperiment',
            name='experiment_instances',
        ),
        migrations.AddField(
            model_name='experimentinstance',
            name='experiment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='experiment', to='common.mtexperiment'),
        ),
    ]
