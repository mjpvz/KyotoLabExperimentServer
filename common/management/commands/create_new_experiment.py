import os
import shutil
from common.models import MtExperiment
from django.db import IntegrityError
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Create a new experiment and the required folders/files'

    def handle(self, *args, **kwargs):
        experiment_name = input("What is the name of your new experiment?\n")
        experiment_name = experiment_name.replace(' ','_')
        try:
            experiment = MtExperiment.objects.create(experiment_slug=experiment_name)
        except IntegrityError as e:
            raise Exception('An experiment already exists with this exact name. Please run again and choose another.')


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
        shutil.copyfile(
            os.path.join('experiments','.templates','create_new_experiment_instance.py'),
            os.path.join(experiment_folder, 'create_new_experiment_instance.py')
        )


        print("The experimental folder has been created! It can be found at {}".format(experiment_folder))
    


