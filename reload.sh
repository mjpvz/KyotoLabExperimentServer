#!/bin/bash
/home/labExperiment/common/management/commands/reload_gunicorn.sh
python /home/labExperiment/common/management/commands/move_files_to_static.py

echo "Reloading..!"