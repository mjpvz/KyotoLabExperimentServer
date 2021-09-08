#!/bin/bash

# Run this command after making code changes to be reflected on the website

sudo systemctl stop gunicorn
sudo systemctl start gunicorn
