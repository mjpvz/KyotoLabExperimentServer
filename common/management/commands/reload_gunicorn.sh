#!/bin/bash

# Run this command after making code changes to be reflected on the website

sudo systemctl stop gunicorn
sudo systemctl start gunicorn

# To debug and see views.py print output stop gunicorn and  run
# gunicorn --bind unix:/home/labExperiment/labExperiment.sock labExperiment.wsgi:application on the CLI