from celery import shared_task
from celery.utils.log import get_task_logger


from django.http import HttpResponse
from django.db.utils import IntegrityError

from labExperiment import settings
from common.models import ExperimentWorker, MtHit, \
        MtAssignment

import os
import json

loggin = get_task_logger('labexperiment.tasks')

# If anything is changed in these files Celery must be started again

@shared_task
def save_submission_data(data):
    # generate file name and saving location
    target_file_name = '_'.join( [data['experiment_name'], data['experiment_instance'], data['condition'], '.txt']) # join results in _.txt but that's fine
    target_dir = os.path.join('experiments','current', data['experiment_name'] ,'data')
    target_file = os.path.join(target_dir, target_file_name)

    with open(target_file, 'a') as f: # Append to current file, create if needed
        f.write(json.dumps(data))
        f.write('\n')

    loggin.info("Returning http response")
    return HttpResponse('Ok!')


@shared_task
def data_submission_outside_amt(data):
    loggin.info("Submission from outside AMT")
    return save_submission_data(data)


@shared_task
def log_hit(**kwargs):
    log_file = 'hit_log_file.txt'

    # First time write headers to the logfile
    if not os.path.exists(log_file):
        with open(log_file, 'a') as f:
            for arg in kwargs:
                f.write(arg)
                f.write(',')
            f.write('\n')

    with open(log_file,'a') as f:
        for arg in kwargs:
            f.write(str(kwargs[arg]))
            f.write(',')
        f.write('\n')

@shared_task
def data_submission_inside_atm(data):
    loggin.info("Submission from inside AMT")
    loggin.info("sandbox: {}".format(settings.MTURK_SANDBOX))


    # Save the experiment instance for this worker
    experiment_worker = ExperimentWorker.objects.get(
        worker__amazon_worker_id=data['worker_id'],
        experiment__experiment_name=data['experiment_name'],)
    experiment_worker.experiment_instance = experiment_worker.experiment.experiment_instances.get(
        experiment_instance_name = data['experiment_instance'],
        condition =  data['condition'],
    )
    #     # Sync the MTHit
    hit = MtHit.objects.get(mturk_id=data['HITid'])
    hit.workers.add(experiment_worker)
    hit.save()
    hit.sync_status(sync_assignments=False) # it might need to be completed multiple times before set to 

        # Generate and store the assignment
    loggin.info("Worker: {}".format(experiment_worker.worker))
    loggin.info("payload: {}".format(data['payload']))

    try: 
        assignment, created = MtAssignment.objects.get_or_create(
            mturk_id = data['assignmentId'],
            hit = hit, 
            experiment_instance__experiment_instance_name = data['experiment_instance'],
            experiment__experiment_name =data['experiment_name'],
            worker = experiment_worker.worker,
            experiment_worker = experiment_worker,
            post_data = data['payload'], # backup
            user_data = data['userData'],
        )

        assignment.save()
        experiment_worker.save()

    except IntegrityError as e:
        loggin.info(e)
        print('Submitting a hit that was already submitted. This happens either during debugging or mturk spamming')

    # Now actually store the data 
    return save_submission_data(data)



