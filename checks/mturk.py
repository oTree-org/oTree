from django.template.loader import select_template
from django.contrib import messages

from otree.views import Page, WaitPage
import otree.common_internal
from otree.checks.templates import check_next_button


class MTurkValidator(object):
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
        missing_next_button_pages = []
        for app in self.session.config['app_sequence']:
            views_module = otree.common_internal.get_pages_module(app)
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
                        missing_next_button_pages.append((page, path_template))
        return missing_next_button_pages

    def validation_message(self):
        missing_next_button_pages = self.get_no_next_buttons_pages()
        if missing_next_button_pages:
            page_listing = '; '.join([
                'Template {} for page {}'.format(template_name, page.__class__.__name__)
                for page, template_name in missing_next_button_pages])
            return (
                'The following templates appear to have no next button. <{}> ' 
                'When using oTree on MTurk, even the last page should have a next button. '
            ).format(page_listing)

        return ''
        # 2017-05-06: I removed the check for timeouts, because I added
        # get_timeout_seconds.
        # i could base the warning on whether timeout_seconds is defined,
        # but it seems like the warning would generate false positives.
        # It's a bit complicated, and doesn't seem worth the code complexity.


    def app_has_no_wait_pages(self, app):
        views_module = otree.common_internal.get_pages_module(app)
        return not any(issubclass(page_class, WaitPage)
                       for page_class in views_module.page_sequence)


