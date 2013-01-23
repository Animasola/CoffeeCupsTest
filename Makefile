MANAGE=django-admin.py

test:
	PYTHONPATH=`pwd` DJANGO_SETTINGS_MODULE=testproject.settings $(MANAGE) test testapp

syncdb:
	PYTHONPATH=`pwd` DJANGO_SETTINGS_MODULE=testproject.settings $(MANAGE) syncdb --noinput

run:
	PYTHONPATH=`pwd` DJANGO_SETTINGS_MODULE=testproject.settings $(MANAGE) runserver

migrate:
	PYTHONPATH=`pwd` DJANGO_SETTINGS_MODULE=testproject.settings $(MANAGE) migrate testapp

