import os
import shutil
import json
import subprocess

from django.db import IntegrityError
from django.core.management.base import BaseCommand

from common.models import MtExperiment
from common.models import MtExperiment, ExperimentInstance, MtHit
from labExperiment import settings


class Command(BaseCommand):
    help = 'Execute an experiment'

    def add_arguments(self, parser):
        parser.add_argument('--experiment', type=str)
        parser.add_argument('--experiment_instance', type=str)

    def handle(self, *args, **options):

        # Make sure that we reload gunicorn and the static fils so everything is in order
        subprocess.check_call('./reload.sh')

        experiment = options['experiment']
        instance = options['experiment_instance']

        # get the data from the config.json file and execute that

        json_file = os.path.join('experiments','current',experiment, 'config.json')
        print(json_file)
        with open(json_file, 'r') as f:
            json_data = json.load(f)
        current_instance_to_run = json_data['experiment_instance'][instance]


        experiment = MtExperiment.objects.get(experiment_name=experiment)

        conditions = current_instance_to_run['conditions']
        participants = int(current_instance_to_run['participants'])
        reward = float(current_instance_to_run['reward'])
        title = current_instance_to_run['title']
        description = current_instance_to_run['description']
        keywords = current_instance_to_run['keywords']
        if 'qualifications' in current_instance_to_run:
            qualifications = current_instance_to_run['qualifications']
        else:
            qualifications = ''

        print("Will post hits to {}".format('sandbox' if settings.MTURK_SANDBOX else 'production'))

        for condition in conditions:
            condition = int(condition)

                # Only one experiment_instance can exist for a name/condition combination.
                # Otherwise, the hit_type_id will no longer match and data submission will thrown an error with .get()
            experiment_instance, created = experiment.experiment_instances.get_or_create(
                experiment_instance_name = instance,
                condition = condition)

                # If not identical, it should be updated 
            updated = False
            if not experiment_instance.reward == reward:
                experiment_instance.reward = reward
                updated = True
            if not experiment_instance.title == title:
                experiment_instance.title = title
                updated = True
            if not experiment_instance.description == description:
                experiment_instance.description = description
                updated = True
            if not experiment_instance.keywords == keywords:
                experiment_instance.keywords = keywords
                updated = True
            if not experiment_instance.num_assignments == participants:
                experiment_instance.num_assignments = participants
                updated = True
            if not experiment_instance.qualifications == json.dumps(qualifications):
                experiment_instance.qualifications = json.dumps(qualifications)
                updated = True

            experiment_instance.save(renew_hit_type_id=updated) # request AMT for a hit_type_id when saving the object

            hit = experiment_instance.hits.create()
            print("Created hit for {} participants. Id={}, Mturk_id={}".format(participants, hit.id, hit.mturk_id))
            


def updated_if_needed(instance, field):
    if not instance.field == field:
        instance.field = field
        return True, instance
    return False, instance

## TODO
"""
Create hits through the hit_id leaves spaces for errors since I'm not actually logging the HIT id.
There can be only one experiment_instance per experiment/condition/instance. 
If there are more, it will be impossible to select it on submission
So either make a hit_id model for sandbox/production 
or make hits directly and individually


"""