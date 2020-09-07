from otree.extensions import get_extensions_modules, get_extensions_data_export_views
import inspect
from importlib import import_module
from django.conf import urls
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic.base import RedirectView
from django.conf import settings
from django.contrib.auth.decorators import login_required
from otree import common_internal


ALWAYS_UNRESTRICTED = {
    'AssignVisitorToRoom',
    'InitializeParticipant',
    'MTurkLandingPage',
    'MTurkStart',
    'JoinSessionAnonymously',
    'OutOfRangeNotification',
    'ParticipantRoomHeartbeat',
    'ParticipantHeartbeatGBAT',
}


UNRESTRICTED_IN_DEMO_MODE = ALWAYS_UNRESTRICTED.union({
    'AdminReport',
    'AdvanceSession',
    'CreateDemoSession',
    'DemoIndex',
    'SessionSplitScreen',
    'SessionDescription',
    'SessionMonitor',
    'SessionPayments',
    'SessionData',
    'SessionStartLinks',
})


def view_classes_from_module(module_name):
    views_module = import_module(module_name)

    # what about custom views?
    return [
        ViewCls for _, ViewCls in inspect.getmembers(views_module)
        if hasattr(ViewCls, 'url_pattern') and
        inspect.getmodule(ViewCls) == views_module
    ]


def url_patterns_from_app_pages(module_name, name_in_url):
    views_module = import_module(module_name)

    view_urls = []
    for ViewCls in views_module.page_sequence:

        url_pattern = ViewCls.url_pattern(name_in_url)
        url_name = ViewCls.url_name()
        view_urls.append(
            urls.url(url_pattern, ViewCls.as_view(), name=url_name)
        )

    return view_urls


def url_patterns_from_builtin_module(module_name: str):

    all_views = view_classes_from_module(module_name)

    view_urls = []
    for ViewCls in all_views:
        # automatically assign URL name for reverse(), it defaults to the
        # class's name
        url_name = getattr(ViewCls, 'url_name', ViewCls.__name__)

        if settings.AUTH_LEVEL == 'STUDY':
            unrestricted = url_name in ALWAYS_UNRESTRICTED
        elif settings.AUTH_LEVEL == 'DEMO':
            unrestricted = url_name in UNRESTRICTED_IN_DEMO_MODE
        else:
            unrestricted = True

        if unrestricted:
            as_view = ViewCls.as_view()
        else:
            # i want to use
            # staff_member_required decorator
            # but then .test_auth_level fails on client.get():
            # NoReverseMatch: 'admin' is not a registered namespace
            as_view = login_required(ViewCls.as_view())

        url_pattern = ViewCls.url_pattern
        if callable(url_pattern):
            url_pattern = url_pattern()

        view_urls.append(
            urls.url(url_pattern, as_view, name=url_name)
        )

    return view_urls


def extensions_urlpatterns():

    urlpatterns = []

    for url_module in get_extensions_modules('urls'):
        urlpatterns += getattr(url_module, 'urlpatterns', [])

    return urlpatterns


def extensions_export_urlpatterns():
    view_classes = get_extensions_data_export_views()
    view_urls = []

    for ViewCls in view_classes:
        if settings.AUTH_LEVEL in {'DEMO', 'STUDY'}:
            as_view = login_required(ViewCls.as_view())
        else:
            as_view = ViewCls.as_view()
        view_urls.append(urls.url(ViewCls.url_pattern, as_view, name=ViewCls.url_name))

    return view_urls


import django.contrib.auth.views as auth_views

class LoginView(auth_views.LoginView):
    template_name = 'otree/login.html'

class LogoutView(auth_views.LogoutView):
    next_page = 'DemoIndex'


def get_urlpatterns():

    urlpatterns = [
        urls.url(r'^$', RedirectView.as_view(url='/demo', permanent=True)),
        urls.url(
            r'^accounts/login/$',
            LoginView.as_view(),
            name='login',
        ),
        urls.url(
            r'^accounts/logout/$',
            LogoutView.as_view(),
            name='logout',
        ),
    ]

    urlpatterns += staticfiles_urlpatterns()

    used_names_in_url = set()
    for app_name in settings.INSTALLED_OTREE_APPS:
        models_module = common_internal.get_models_module(app_name)
        name_in_url = models_module.Constants.name_in_url
        if name_in_url in used_names_in_url:
            msg = (
                "App {} has Constants.name_in_url='{}', "
                "which is already used by another app"
            ).format(app_name, name_in_url)
            raise ValueError(msg)

        used_names_in_url.add(name_in_url)

        views_module = common_internal.get_pages_module(app_name)
        urlpatterns += url_patterns_from_app_pages(
            views_module.__name__, name_in_url)


    urlpatterns += url_patterns_from_builtin_module('otree.views.participant')
    urlpatterns += url_patterns_from_builtin_module('otree.views.demo')
    urlpatterns += url_patterns_from_builtin_module('otree.views.admin')
    urlpatterns += url_patterns_from_builtin_module('otree.views.room')
    urlpatterns += url_patterns_from_builtin_module('otree.views.mturk')
    urlpatterns += url_patterns_from_builtin_module('otree.views.export')

    urlpatterns += extensions_urlpatterns()
    urlpatterns += extensions_export_urlpatterns()

    # serve an empty favicon?
    # otherwise, the logs will contain:
    # [WARNING] django.request > Not Found: /favicon.ico
    # Not Found: /favicon.ico
    # don't want to add a <link> in base template because even if it exists,
    # browsers will still request /favicon.ico.
    # plus it makes the HTML noisier
    # can't use the static() function here because maybe collectstatic
    # has not been run yet
    # and it seems an empty HttpResponse or even a 204 response makes the browser
    # just keep requesting the file with every page load
    # hmmm...now it seems that chrome is not re-requesting with every page load
    # but firefox does. but if i remove the favicon, there's 1 404 then FF doesn't
    # ask for it again.


    # import os
    # dir_path = os.path.dirname(os.path.realpath(__file__))
    # with open(os.path.join(dir_path, 'favicon_invisible.ico'), 'rb') as f:
    # #with open('favicon.ico', 'rb') as f:
    #     favicon_content = f.read()
    #
    #
    # urlpatterns.append(
    #     urls.url(
    #         r'^favicon\.ico$',
    #         lambda request: HttpResponse(favicon_content, content_type="image/x-icon")
    #     )
    # )

    return urlpatterns


urlpatterns = get_urlpatterns()
