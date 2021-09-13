import os
import shutil
from common.models import MtExperiment
from django.db import IntegrityError
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Create a new experiment and the required folders/files'

    def add_arguments(self, parser):
        parser.add_argument('--experiment', type=str)

    def handle(self, *args, **options):
        experiment_name = options['experiment']
        if not experiment_name:
            raise Exception("Call this function by providing an experiment name like ./manage.py create_new_experiment --experiment NAME")
        experiment_name = experiment_name.replace(' ','_') # don't allow spaces

        try:
            experiment = MtExperiment.objects.create(experiment_name=experiment_name)
        except IntegrityError as e:
            raise Exception('An experiment already exists with the exact name {}. Please run again and choose another.'.format(experiment_name))


        experiment_folder = os.path.join('experiments','current',experiment_name)
        # make folder structure
        os.mkdir(experiment_folder) # main folder
        os.mkdir(os.path.join(experiment_folder, 'stimuli')) 
        os.mkdir(os.path.join(experiment_folder, 'data')) 
        os.mkdir(os.path.join(experiment_folder, 'files')) 


        # copy the required files. 
        shutil.copyfile(
            os.path.join('experiments','.templates','config.json'),
            os.path.join(experiment_folder, 'config.json')
        )

        print("The experimental folder has been created! It can be found at {}".format(experiment_folder))
    


