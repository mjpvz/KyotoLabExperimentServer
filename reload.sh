#!/bin/bash
./common/management/commands/reload_gunicorn.sh
python ./common/management/commands/move_files_to_static.py

