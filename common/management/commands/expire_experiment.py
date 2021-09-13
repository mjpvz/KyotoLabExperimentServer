import os
import shutil
from common.models import MtExperiment
from django.db import IntegrityError
from django.core.management.base import BaseCommand
import json
from common.models import MtExperiment, ExperimentInstance, MtHit
from mturk.utils import get_mturk_connection

class Command(BaseCommand):
    """Expire all hits for a certain experiment/instance combination.
        Can be executed by ./manage.py expire_experiment --experiment test001 --experiment_instance v1

    """



    def add_arguments(self, parser):
        parser.add_argument('--experiment', type=str)
        parser.add_argument('--experiment_instance', type=str)

    def handle(self, *args, **options):

        # Make sure all required files are there
        from common.management.commands.move_files_to_static import move_files
        move_files()

        experiment = options['experiment']
        experiment = MtExperiment.objects.get(experiment_name=experiment)
        if not experiment:
            raise Exception('You must run this command with an experiment, like so: ./manage.py expire_experiment --experiment YOUR_EXP_NAME')

        instance = options['experiment_instance']
        if instance:
            instances = experiment.experiment_instances.filter(experiment_instance_name=instance)
        else:
            print("Expiring all hits for this experiment..")
            instances = experiment.experiment_instances.all()

        for instance in instances:
            instance.expire_all_hits()

            

            
