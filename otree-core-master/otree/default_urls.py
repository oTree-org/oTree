from django.conf.urls import patterns
import otree.urls

urlpatterns = patterns('',)

otree.urls.augment_urlpatterns(urlpatterns)
