from django.conf.urls import *
import ptree.urls
from ptree.adminlib import autodiscover

autodiscover()

urlpatterns = patterns('',)

ptree.urls.augment_urlpatterns(urlpatterns)