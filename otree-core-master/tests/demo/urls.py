from django.conf.urls import patterns, url


urlpatterns = patterns(
    '',
    url(r'^$', 'tests.demo.views.index', name='index'),
    url(r'^latex/$', 'django.shortcuts.render',
        {'template_name': 'demo/latex.html'}, name='latex'),
    url(r'^widgets/$', 'tests.demo.views.widgets', name='widgets'),
    url(r'^fields/$', 'tests.demo.views.modelformfields',
        name='modelformfields'),
)
