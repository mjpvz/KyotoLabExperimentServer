from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from labExperiment import settings
from labExperiment.tasks import data_submission_outside_amt, data_submission_inside_atm
from common.models import MtExperiment, ExperimentWorker, UserProfile, MtHit, \
        MtAssignment

import os
import json
import time

from celery.utils.log import get_task_logger
loggin = get_task_logger('labexperiment.views')

# The Print statements are send to the gunicorn log, which I can't find. 
# TO debug, use the reload command first and then manually bind gunicorn to the socket. This will make all these print statements
# appear on the CLI
# gunicorn --bind unix:/home/labExperiment/labExperiment.sock labExperiment.wsgi:application
# Once done be sure to hit reload again

def globalIndx(request):
    return HttpResponse('You are not supposed to be here. If you are an AMT participant, please contact the requester. Our aplogies for any inconvience. ')

def experiment(request, experiment_name, experiment_instance, condition):
    # define context used to populate the django template
    context = {
        'experiment_name' : experiment_name,
        'experiment_instance' : experiment_instance,
        'condition':condition,
        'sandbox': settings.MTURK_SANDBOX
    }
    # We will load the specific html file related to this experiment, which in turn will be placed within the experiment_wrappr.html located in common/templates
    html_file = os.path.join(experiment_name, 'files', experiment_instance + '.html')
    return render(request, html_file, context)


def data_submission(request):
    # Access and load stringified data
    data = json.loads(request.GET.get('data','did not work'))

    if not data['assignmentId'] and not data['HITid']:
        response =  data_submission_outside_amt.apply_async(
            kwargs={'data' : data}, retry=True, retry_policy={'max_retries': 100}
        )

    else:
        response =  data_submission_inside_atm.apply_async(
            kwargs={'data' : data}, retry=True, retry_policy={'max_retries': 100}
        )
    return HttpResponse('Ok')



def workerCheck(request):

    loggin.info("Worker check")
    worker_id = request.GET.get('worker_id', False)
    experiment_name = request.GET.get('experiment_name', False)

    if not worker_id and experiment_name:
        raise Exception("Data was not transmitted properly")

    experiment = MtExperiment.objects.get(experiment_name = experiment_name)
    user, created = UserProfile.objects.get_or_create(
        amazon_worker_id=worker_id)

    experiment_worker, created = ExperimentWorker.objects.get_or_create(
        experiment=experiment, 
        worker=user)

    if created:
        return HttpResponse('Not found')
    else: 
        return HttpResponse('Found')

