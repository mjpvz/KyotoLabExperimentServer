# Generated by Django 3.2.7 on 2021-09-09 04:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0007_rename_new_hit_settings_mtexperiment_experiment_instance'),
    ]

    operations = [
        migrations.RenameField(
            model_name='experimentinstance',
            old_name='experiment_instance_slug',
            new_name='experiment_instance_name',
        ),
        migrations.AddField(
            model_name='experimentworker',
            name='submitted_work',
            field=models.BooleanField(default=False),
        ),
    ]
