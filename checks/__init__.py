import inspect
import io
import os

from otree import common_internal
from importlib import import_module

from django.apps import apps
from django.conf import settings
from django.core.checks import register, Error, Warning
import django.db.models.fields
from otree.api import (
    BasePlayer, BaseGroup, BaseSubsession, Currency, WaitPage, Page)
from otree.common_internal import _get_all_configs
from pathlib import Path
import re


class AppCheckHelper:
    """Basically a wrapper around the AppConfig
    """

    def __init__(self, app_config, errors):
        self.app_config = app_config
        self.errors = errors

    def add_error(self, title, numeric_id: int, **kwargs):
        issue_id = 'otree.E' + str(numeric_id).zfill(3)
        kwargs.setdefault('obj', self.app_config.label)
        return self.errors.append(Error(title, id=issue_id, **kwargs))

    def add_warning(self, title, numeric_id: int, **kwargs):
        kwargs.setdefault('obj', self.app_config.label)
        issue_id = 'otree.W' + str(numeric_id).zfill(3)
        return self.errors.append(Warning(title, id=issue_id, **kwargs))

    # Helper meythods

    def get_path(self, name):
        return os.path.join(self.app_config.path, name)

    def get_rel_path(self, name):
        basepath = os.getcwd()
        return os.path.relpath(name, basepath)

    def get_module(self, name):
        return import_module(self.app_config.name + '.' + name)

    def get_template_names(self):
        path = self.get_path('templates')
        template_names = []
        for root, dirs, files in os.walk(path):
            for filename in [f for f in files if f.endswith('.html')]:
                template_names.append(os.path.join(root, filename))
        return template_names

    def module_exists(self, module):
        try:
            self.get_module(module)
            return True
        except ImportError as e:
            return False

    def class_exists(self, module, name):
        module = self.get_module(module)
        cls = getattr(module, name, None)
        return inspect.isclass(cls)


# CHECKS

def files(helper: AppCheckHelper, **kwargs):
    # don't check views.py because it might be pages.py
    for fn in ['models.py']:
        if not os.path.isfile(helper.get_path(fn)):
            helper.add_error(
                'No "%s" file found in game folder' % fn,
                numeric_id=102
            )

    templates_dir = Path(helper.get_path('templates'))
    app_label = helper.app_config.label
    if templates_dir.is_dir():
        # check for files in templates/, but not in templates/<label>
        misplaced_files = list(templates_dir.glob('*.html'))
        if misplaced_files:
            hint = (
                'Move template files from "{app}/templates/" '
                'to "{app}/templates/{app}" subfolder'.format(
                    app=app_label)
            )

            helper.add_error(
                "Templates files in wrong folder",
                hint=hint, numeric_id=103,
            )

        all_subfolders = set(templates_dir.glob('*/'))
        correctly_named_subfolders = set(
            templates_dir.glob('{}/'.format(app_label)))
        other_subfolders = all_subfolders - correctly_named_subfolders
        if other_subfolders and not correctly_named_subfolders:
            msg = (
                "The 'templates' folder has a subfolder called '{}', "
                "but it should be renamed '{}' to match the name of the app. "
            ).format(other_subfolders.pop().name, app_label)
            helper.add_error(msg, numeric_id=104)


base_model_attrs = {
    'Player': set(dir(BasePlayer)),
    'Group': set(dir(BaseGroup)),
    'Subsession': set(dir(BaseSubsession)),
}

model_field_substitutes = {
    int: 'IntegerField',
    float: 'FloatField',
    bool: 'BooleanField',
    str: 'CharField',
    Currency: 'CurrencyField',
    type(None): 'IntegerField'
    # not always int, but it's a reasonable suggestion
}


def model_classes(helper: AppCheckHelper, **kwargs):
    for name in ['Subsession', 'Group', 'Player']:
        try:
            helper.app_config.get_model(name)
        except LookupError:
            helper.add_error(
                'MissingModel: Model "%s" not defined' % name, numeric_id=110)

    app_config = helper.app_config
    Player = app_config.get_model('Player')
    Group = app_config.get_model('Group')
    Subsession = app_config.get_model('Subsession')

    for Model in [Player, Group, Subsession]:
        for attr_name in dir(Model):
            if attr_name not in base_model_attrs[Model.__name__]:
                try:
                    attr_value = getattr(Model, attr_name)
                    _type = type(attr_value)
                except AttributeError:
                    # I got "The 'q_country' attribute can only be accessed
                    # from Player instances."
                    # can just filter/ignore these.
                    pass
                else:
                    if _type in model_field_substitutes.keys():
                        msg = (
                            'NonModelFieldAttr: '
                            '{} has attribute "{}", which is not a model field, '
                            'and will therefore not be saved '
                            'to the database.'.format(Model.__name__,
                                                      attr_name))

                        helper.add_error(
                            msg,
                            numeric_id=111,
                            hint='Consider changing to "{} = models.{}(initial={})"'.format(
                                attr_name, model_field_substitutes[_type],
                                repr(getattr(Model, attr_name)))
                        )
                    # if people just need an iterable of choices for a model field,
                    # they should use a tuple, not list or dict
                    elif _type in {list, dict, set}:
                        warning = (
                            'MutableModelClassAttr: '
                            '{ModelName}.{attr} is a {type_name}. '
                            'Modifying it during a session (e.g. appending or setting values) '
                            'will have unpredictable results; '
                            'you should use '
                            'session.vars or participant.vars instead. '
                            'Or, if this {type_name} is read-only, '
                            "then it's recommended to move it outside of this class "
                            '(e.g. put it in Constants).'
                        ).format(ModelName=Model.__name__,
                                 attr=attr_name,
                                 type_name=_type.__name__)

                        helper.add_error(warning, numeric_id=112)
                    # isinstance(X, type) means X is a class, not instance
                    elif (isinstance(attr_value, type) and
                              issubclass(attr_value,
                                         django.db.models.fields.Field)):
                        msg = (
                            '{}.{} is missing parentheses.'
                        ).format(Model.__name__, attr_name)
                        helper.add_error(
                            msg, numeric_id=113,
                            hint=(
                                'Consider changing to "{} = models.{}()"'
                            ).format(attr_name, attr_value.__name__)
                        )


def constants(helper: AppCheckHelper, **kwargs):
    if not helper.module_exists('models'):
        return
    if not helper.class_exists('models', 'Constants'):
        helper.add_error(
            'models.py does not contain Constants class', numeric_id=11
        )
        return

    models = helper.get_module('models')
    Constants = getattr(models, 'Constants')
    attrs = ['name_in_url', 'players_per_group', 'num_rounds']
    for attr_name in attrs:
        if not hasattr(Constants, attr_name):
            msg = "models.py: 'Constants' class needs to define '{}'"
            helper.add_error(msg.format(attr_name), numeric_id=12)
    ppg = Constants.players_per_group
    if ppg == 0 or ppg == 1:
        helper.add_error(
            "models.py: Constants.players_per_group cannot be {}. You "
            "should set it to None, which makes the group "
            "all players in the subsession.".format(ppg),
            numeric_id=13
        )
    if ' ' in Constants.name_in_url:
        helper.add_error(
            "models.py: Constants.name_in_url must not contain spaces",
            numeric_id=14
        )


def pages_function(helper: AppCheckHelper, **kwargs):
    pages_module = common_internal.get_pages_module(helper.app_config.name)
    views_or_pages = pages_module.__name__.split('.')[-1]
    try:
        page_list = pages_module.page_sequence
    except:
        helper.add_error(
            '{}.py is missing the variable page_sequence.'.format(
                views_or_pages),
            numeric_id=21
        )
        return
    else:
        for i, ViewCls in enumerate(page_list):
            # there is no good reason to include Page in page_sequence.
            # As for WaitPage: even though it works fine currently
            # and can save the effort of subclassing,
            # we should restrict it, because:
            # - one user had "class WaitPage(Page):".
            # - if someone makes "class WaitPage(WaitPage):", they might
            #   not realize why it's inheriting the extra behavior.
            # overall, I think the small inconvenience of having to subclass
            # once per app
            # is outweighed by the unexpected behavior if someone subclasses
            # it without understanding inheritance.
            # BUT: built-in Trust game had a wait page called WaitPage.
            # that was fixed on Aug 24, 2017, need to wait a while...
            # see below in ensure_no_misspelled_attributes,
            # we can get rid of a check there also
            if ViewCls.__name__ == 'Page':
                msg = (
                    "page_sequence cannot contain "
                    "a class called 'Page'."
                )
                helper.add_error(msg, numeric_id=22)
            if ViewCls.__name__ == 'WaitPage' and helper.app_config.name != 'trust':
                msg = (
                    "page_sequence cannot contain "
                    "a class called 'WaitPage'."
                )
                helper.add_error(msg, numeric_id=221)

            if issubclass(ViewCls, WaitPage):
                if ViewCls.group_by_arrival_time:
                    if i > 0:
                        helper.add_error(
                            '"{}" has group_by_arrival_time=True, so '
                            'it must be placed first in page_sequence.'.format(
                                ViewCls.__name__), numeric_id=23)
                    if ViewCls.wait_for_all_groups:
                        helper.add_error(
                            'Page "{}" has group_by_arrival_time=True, so '
                            'it cannot have wait_for_all_groups=True also.'.format(
                                ViewCls.__name__), numeric_id=24)
                # alternative technique is to not define the method on WaitPage
                # and then use hasattr, but I want to keep all complexity
                # out of views.abstract
                elif (
                            ViewCls.get_players_for_group != WaitPage.get_players_for_group):
                    helper.add_error(
                        'Page "{}" defines get_players_for_group, '
                        'but in order to use this method, you must set '
                        'group_by_arrival_time=True'.format(
                            ViewCls.__name__), numeric_id=25)
            elif issubclass(ViewCls, Page):
                pass  # ok
            else:
                msg = '"{}" is not a valid page'.format(ViewCls)
                helper.add_error(msg, numeric_id=26)

            ensure_no_misspelled_attributes(ViewCls, helper)


def ensure_no_misspelled_attributes(ViewCls: type, helper: AppCheckHelper):
    '''just a helper function'''

    # this messes with the logic of base classes.
    # do this instead of ViewCls == WaitPage, because _builtin already
    # subclasses it, so you would get a warning like:
    # Page "WaitPage" has the following method that is not recognized by oTree:
    # "z_autocomplete".
    if ViewCls.__name__ == 'WaitPage' or ViewCls.__name__ == 'Page':
        return

    # make sure no misspelled attributes
    base_members = set()
    for Cls in ViewCls.__bases__:
        base_members.update(dir(Cls))
    child_members = set(dir(ViewCls))
    child_only_members = child_members - base_members

    dynamic_form_methods = set()  # needs to be a set
    for member in child_only_members:
        # error_message, not _error_message
        for valid_ending in ['error_message', '_min', '_max', '_choices']:
            if member.endswith(valid_ending):
                dynamic_form_methods.add(member)
    invalid_members = child_only_members - dynamic_form_methods
    if invalid_members:
        ALLOW_CUSTOM_ATTRIBUTES = '_allow_custom_attributes'
        if getattr(ViewCls, ALLOW_CUSTOM_ATTRIBUTES, False):
            return

        page_attrs = set(dir(Page))
        wait_page_attrs = set(dir(WaitPage))
        ATTRS_ON_PAGE_ONLY = page_attrs - wait_page_attrs
        ATTRS_ON_WAITPAGE_ONLY = wait_page_attrs - page_attrs

        for member in invalid_members:
            # this assumes that ViewCls is a Page or WaitPage
            if member in ATTRS_ON_PAGE_ONLY:
                assert issubclass(ViewCls, WaitPage), (ViewCls, member)
                msg = (
                    'WaitPage "{ViewClsName}" has the attribute "{member}" that is not '
                    'allowed on a WaitPage. '
                )
                numeric_id = 27
            elif member in ATTRS_ON_WAITPAGE_ONLY:
                assert issubclass(ViewCls, Page), (ViewCls, member)
                msg = (
                    'Page "{ViewClsName}" has the attribute "{member}" that is '
                    'only allowed on a WaitPage, not a regular Page. '
                )
                numeric_id=271
            elif callable(getattr(ViewCls, member)):
                msg = (
                    'Page "{ViewClsName}" has the following method that is not '
                    'recognized by oTree: "{member}". '
                    'Consider moving it into '
                    'the Player class in models.py. '
                )

                numeric_id=28
            else:
                msg = (
                    'Page "{ViewClsName}" has the following attribute that is not '
                    'recognized by oTree: "{member}". '
                )
                numeric_id=29

            fmt_kwargs = {
                'ViewClsName': ViewCls.__name__,
                'FLAG': ALLOW_CUSTOM_ATTRIBUTES,
                'member': member,
            }
            # when i make this an error, should add this workaround.
            #msg +=  'If you want to keep it here, you need to set '
            #        '{FLAG}=True on the page class.'

            # at first, just make it a warning.
            helper.add_error(msg.format(**fmt_kwargs), numeric_id)


def unique_sessions_names(helper: AppCheckHelper, **kwargs):
    already_seen = set()
    for st in settings.SESSION_CONFIGS:
        st_name = st["name"]
        if st_name in already_seen:
            msg = "Duplicate SESSION_CONFIG name '{}'".format(st_name)
            helper.add_error(msg, numeric_id=40)
        else:
            already_seen.add(st_name)


def unique_room_names(helper: AppCheckHelper, **kwargs):
    already_seen = set()
    for room in getattr(settings, 'ROOMS', []):
        room_name = room["name"]
        if room_name in already_seen:
            msg = "Duplicate ROOM name '{}'".format(room_name)
            helper.add_error(msg, numeric_id=50)
        else:
            already_seen.add(room_name)


def template_encoding(helper: AppCheckHelper, **kwargs):
    from otree.checks.templates import has_valid_encoding
    for template_name in helper.get_template_names():
        if not has_valid_encoding(template_name):
            helper.add_error(
                'The template {template} is not UTF-8 encoded. '
                'Please configure your text editor to always save files '
                'as UTF-8. Then open the file and save it again.'
                    .format(template=helper.get_rel_path(template_name)),
                numeric_id=60,
            )


def make_check_function(func):
    def check_function(app_configs, **kwargs):
        # if app_configs list is given (e.g. otree check app1 app2), run on those
        # if it's None, run on all apps
        # (system check API requires this)
        app_configs = app_configs or _get_all_configs()
        errors = []
        for app_config in app_configs:
            helper = AppCheckHelper(app_config, errors)
            func(helper, **kwargs)
        return errors

    return check_function


def make_check_function_run_once(func):
    def check_function(app_configs, **kwargs):
        otree_app_config = apps.get_app_config('otree')
        # ignore app_configs list -- just run once
        errors = []
        helper = AppCheckHelper(otree_app_config, errors)
        func(helper, **kwargs)
        return errors

    return check_function


def register_system_checks():
    for func in [
        unique_room_names,
        unique_sessions_names,
    ]:
        check_function = make_check_function_run_once(func)
        register(check_function)

    for func in [
        model_classes,
        files,
        constants,
        pages_function,
        template_encoding,
    ]:
        check_function = make_check_function(func)
        register(check_function)
