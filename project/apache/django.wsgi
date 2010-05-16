import os, sys

sys.path.append('/Library/Webserver/Documents/Django')
os.environ['DJANGO_SETTINGS_MODULE'] = 'project.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
