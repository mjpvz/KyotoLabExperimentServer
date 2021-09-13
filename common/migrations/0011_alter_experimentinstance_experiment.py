# Generated by Django 3.2.7 on 2021-09-09 04:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0010_auto_20210909_0437'),
    ]

    operations = [
        migrations.AlterField(
            model_name='experimentinstance',
            name='experiment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='experiments', to='common.mtexperiment'),
        ),
    ]
