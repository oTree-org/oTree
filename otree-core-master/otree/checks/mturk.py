from django.template.loader import select_template
from django.contrib import messages

from otree.views import Page, WaitPage
import otree.common_internal
from otree.checks.templates import check_next_button


class ValidateMTurk(object):
    '''
    This validation is based on issue #314
    '''
    def __init__(self, session):
        self.session = session

    def get_no_next_buttons_pages(self):
        '''
        Check that every page in every app has next_button.
        Also including the last page. Next button on last page is
        necessary to trigger an externalSubmit to the MTurk server.
        '''
        for app in self.session.config['app_sequence']:
            views_module = otree.common_internal.get_views_module(app)
            for page_class in views_module.page_sequence:
                page = page_class()
                if isinstance(page, Page):
                    path_template = page.get_template_names()
                    template = select_template(path_template)
                    # The returned ``template`` variable is only a wrapper
                    # around Django's internal ``Template`` object.
                    template = template.template
                    if not check_next_button(template):
                        # can't use template.origin.name because it's not
                        # available when DEBUG is off. So use path_template
                        # instead
                        yield page, path_template

    def app_has_no_wait_pages(self, app):
        views_module = otree.common_internal.get_views_module(app)
        return not any(issubclass(page_class, WaitPage)
                       for page_class in views_module.page_sequence)

    def get_no_timeout_pages(self):
        '''
        if an app contains a WaitPage then each Page of that app
        must have a timeout_seconds defined.
        '''
        pages = []
        pages_needs_timeout = False
        for app in self.session.config['app_sequence']:
            views_module = otree.common_internal.get_views_module(app)
            for page_class in views_module.page_sequence:
                page = page_class()
                if isinstance(page, WaitPage):
                    pages_needs_timeout = True
                else:
                    pages.append(page)
        if pages_needs_timeout:
            for page in pages:
                if not page.has_timeout():
                    yield page


def validate_session_for_mturk(request, session):
    v = ValidateMTurk(session)
    for page, template_name in v.get_no_next_buttons_pages():
        messages.warning(
            request,
            ('Template %s for page %s has no next button. '
             'When using oTree on MTurk, '
             'even the last page should have a next button.')
            % (template_name, page.__class__.__name__)
        )
    for page in v.get_no_timeout_pages():
        messages.warning(
            request,
            'Page %s in view %s has no timeout'
            % (page.__class__.__name__, page.__module__)
        )
