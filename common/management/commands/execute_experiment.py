import os
import shutil
from common.models import MtExperiment
from django.db import IntegrityError
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Execute an experiment'

    def add_arguments(self, parser):
        parser.add_argument('--experiment', type=str)
        parser.add_argument('--experiment_instance', type=str)

    def handle(self, *args, **options):

        # Make sure all required files are there
        from move_files_to_static import move_files
        move_files()

        experiment = options['experiment']
        instance = options['experiment_instance']

        # get the data from the config.json file and execute that

        print(experiment)
        print(instance)

    



""" 
    Can be executed by ./manage.py execute_experiment --experiment test001 --experiment_instance v1
    First make sure that the website actually works local
    1) has acces to htlm
    add wrapper around the experimental_instance.html so that it always has some function and always loads in the correct css/js, stimuli and condition data. 
    Actually submit it mturk
    are mturkworker models succesfully created?
    can we block workers?
    See if data is correctly submitted 
    TODO 
"""
