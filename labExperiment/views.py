from django.http import HttpResponse
from django.shortcuts import render
import os


def global_index(request):
    return HttpResponse('You are not supposed to be here. If you are an AMT participant, please contact the requester. Our aplogies for any inconvience. ')

def experiment(request, experiment_name, experiment_instance):
    context = {
        'title' : 'testy title',
        'experiment_name' : experiment_name,
        'experiment_instance' : experiment_instance,
    }
    html_file = os.path.join(experiment_name, 'files', experiment_instance + '.html')
    return render(request, html_file, context)