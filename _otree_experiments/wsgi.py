import os
import django.conf
import settings

if not django.conf.settings.configured:
    django.conf.settings.configure(default_settings=django.conf.global_settings, **settings.settings)

from django.core.wsgi import get_wsgi_application

from dj_static import Cling
application = Cling(get_wsgi_application())