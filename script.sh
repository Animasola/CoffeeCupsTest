#!/bin/sh
python manage.py models_info --settings="testproject.settings" 2>> $(date +"%Y%m%d").dat
