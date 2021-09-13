import json
import os
import shutil

def create_instance():
    experiment_name = os.getcwd().split('/')[-1] 
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    print("The following values can still be changed later in the config.json files if needed")
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    experiment_instance__name = input("What is the name of the new experiment version for the {} experiment?\n".format(experiment_name))

    if os.path.exists(os.path.join('files',experiment_instance__name+'.html')):
        raise Exception("A instance of this experiment with this name already exists. Please try again with a different name.")

    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    participants = input("How many participants should perform {} PER condition?\n".format(experiment_instance__name))
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    conditions = input("How many conditions should there be for {}?\n".format(experiment_instance__name))
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')

        # Add the input data to a json. First open the template json
    config_file = 'config.json'
    with open(config_file,'r') as f:
        data = json.load(f)

        # add the collected data to the config file
    data['experiment_instance'][experiment_instance__name] = {}
    data['experiment_instance'][experiment_instance__name]['participants'] = participants
    data['experiment_instance'][experiment_instance__name]['conditions'] = list(range(int(conditions)))
        # And save the json
    with open(config_file,'w') as f:
        json.dump(data, f, indent=4)


    # Touch css and js files and close them straight away, just to that they are in the right place
    open(os.path.join('files', experiment_instance__name + '.css'),'a').close()
    open(os.path.join('files', experiment_instance__name + '.js'),'a').close()

    # Copy the .html file template
    shutil.copyfile(
        os.path.join('..','..','.templates','default_template.html'),
        os.path.join('files', experiment_instance__name + '.html')
    )

if __name__=="__main__":
    create_instance()
