# Generated by Django 3.2.7 on 2021-09-09 04:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0001_squashed_0012_alter_experimentinstance_experiment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='experimentinstance',
            name='experiment_instance_name',
            field=models.CharField(db_index=True, max_length=32),
        ),
        migrations.AlterField(
            model_name='experimentworker',
            name='experiment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='experiment_workers', to='common.mtexperiment'),
        ),
    ]