
import json
import os
import shutil
from common.models import MtExperiment
from django.db import IntegrityError
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Create a new experiment and the required folders/files'

    def add_arguments(self, parser):
        parser.add_argument('--experiment', type=str)
        parser.add_argument('--experiment_instance', type=str)


    def handle(self, *args, **options):

        experiment_name = options['experiment']
        if not experiment_name:
            raise Exception("Please enter an experiment name. See the readme for an example")
        experiment_name = experiment_name.replace(' ','_') # don't allow spaces

        try:
            experiment = MtExperiment.objects.get(experiment_name=experiment_name)
        except IntegrityError as e:
            raise Exception('No experiment with this name was found. Did you enter the correct name? Entered={}.'.format(experiment_name))

        experiment_instance__name = options['experiment_instance']
        if not experiment_instance__name:
            raise Exception("Please enter an experiment instance name. See the readme for an example")

        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        print('~~~~~~The following values can still be changed later in the config.json files if needed~~~~~~')
        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        
        if os.path.exists(os.path.join('files',experiment_instance__name+'.html')):
            raise Exception("A instance of this experiment with this name already exists. Please try again with a different name.")


        participants = input("How many participants should perform {} PER condition?\n".format(experiment_instance__name))
        conditions = input("How many conditions should there be for {}?\n".format(experiment_instance__name))
        title =  input("What is the title for this experiment? This is what participants will see before clicking our hit.\n")
        description = input('Enter a description for this experiment. This will be shown to participants before accepting the hit.\n')
        keywords = input("Enter keywords for this experiment separated by a space. This will help participants find our experiments.\n")
        reward = input("What should the pay be for each participant (in USD)?\n")


        qualifications = input("Do you want to add the standard qualifications to this hit? y/n")
        while qualifications.lower() not in ['y','n']:
            qualifications = input("Do you want to add the standard qualifications to this hit? Please reply y or n for yes/no")
        if qualifications.lower() == 'n':
            print('If you want to add other qualifications to this hit, you will then have to add them manually.')

            # Add the input data to a json. First open the template json
        file_name = 'config.json'
        file_location = os.path.join('experiments','current',experiment_name)
        file_path = os.path.join(file_location, file_name)
        with open(file_path,'r') as f:
            data = json.load(f)


            # add the collected data to the config file

        data['experiment_instance'][experiment_instance__name] = {}
        data['experiment_instance'][experiment_instance__name]['participants'] = participants
        data['experiment_instance'][experiment_instance__name]['conditions'] = list(range(int(conditions)))
        data['experiment_instance'][experiment_instance__name]['title'] = title
        data['experiment_instance'][experiment_instance__name]['description'] = description
        data['experiment_instance'][experiment_instance__name]['keywords'] = keywords
        data['experiment_instance'][experiment_instance__name]['reward'] = reward
        if qualifications.lower() == 'y':
            data['experiment_instance'][experiment_instance__name]['qualifications'] = {}
            data['experiment_instance'][experiment_instance__name]['qualifications']['num_approved'] = 1000
            data['experiment_instance'][experiment_instance__name]['qualifications']['perc_approved'] = 95
            data['experiment_instance'][experiment_instance__name]['qualifications']['local_requirement'] = 1

            # And save the json
        with open(file_path,'w') as f:
            json.dump(data, f, indent=4)


        # Touch css and js files and close them straight away, just to that they are in the right place
        open(os.path.join(file_location, 'files', experiment_instance__name + '.css'),'a').close()
        open(os.path.join(file_location, 'files', experiment_instance__name + '.js'),'a').close()

        # Copy the .html file template
        shutil.copyfile(
            os.path.join('experiments','.templates','default_template.html'),
            os.path.join(file_location, 'files', experiment_instance__name + '.html')
        )

