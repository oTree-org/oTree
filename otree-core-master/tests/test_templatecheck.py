# -*- coding: utf-8 -*-
import os
from django.core.management import call_command, CommandError
from django.template import Template

from otree.checks.templates import get_unreachable_content, check_next_button
from otree.checks.templates import format_source_snippet
from otree.checks.templates import has_valid_encoding
from .base import TestCase
from .utils import capture_stdout, dummyapp
import six


TEST_DIR = os.path.dirname(os.path.abspath(__file__))


class TemplateCheckContentTest(TestCase):
    def test_non_extending_template(self):
        template = Template('''Stuff in here.''')
        content = get_unreachable_content(template)
        self.assertFalse(content)

        template = Template('''{% block head %}Stuff in here.{% endblock %}''')
        content = get_unreachable_content(template)
        self.assertFalse(content)

        template = Template(
            '''
            Free i am.
            {% block head %}I'm not :({% endblock %}
            ''')
        content = get_unreachable_content(template)
        self.assertEqual(content, [])

    def test_ok_extending_template(self):
        template = Template(
            '''
            {% extends "base.html" %}

            {% block content %}
            Stuff in here.
            {% if 1 %}Un-Conditional{% endif %}
            {% endblock %}
            ''')

        content = get_unreachable_content(template)
        self.assertEqual(content, [])

    def test_extending_template_with_non_wrapped_code(self):
        template = Template(
            '''
            {% extends "base.html" %}

            Free i am.

            {% block content %}Stuff in here.{% endblock %}
            ''')

        content = get_unreachable_content(template)
        self.assertEqual(len(content), 1)
        self.assertTrue('Free i am.' in content[0])
        self.assertTrue('Stuff in here.' not in content[0])

    def test_text_after_block(self):
        template = Template(
            '''
            {% extends "base.html" %}
            {% block content %}Stuff in here.{% endblock %}
            After the block.
            ''')

        content = get_unreachable_content(template)
        self.assertEqual(len(content), 1)
        self.assertTrue('After the block.' in content[0])
        self.assertTrue('Stuff in here.' not in content[0])

    def test_multiple_text_nodes(self):
        template = Template(
            '''
            {% extends "base.html" %}
            First.
            {% block content %}Stuff in here.{% endblock %}
            Second.
            {% load i18n %}
            Third.
            ''')

        content = get_unreachable_content(template)
        self.assertEqual(len(content), 3)
        self.assertTrue('First.' in content[0])
        self.assertTrue('Second.' in content[1])
        self.assertTrue('Third.' in content[2])

    def test_non_block_statements(self):
        # We do not dive into other statements.
        template = Template(
            '''
            {% extends "base.html" %}

            {% if 1 %}
            Free i am.
            {% endif %}
            ''')

        content = get_unreachable_content(template)
        self.assertEqual(len(content), 0)

    def test_ignore_comments(self):
        template = Template(
            '''
            {% extends "base.html" %}
            {# comment #}
            ''')

        content = get_unreachable_content(template)
        self.assertEqual(len(content), 0)

        template = Template(
            '''
            {% extends "base.html" %}
            {% comment %}comment{% endcomment %}
            ''')

        content = get_unreachable_content(template)
        self.assertEqual(len(content), 0)


class TemplateCheckNextButtonTest(TestCase):

    def test_outside_block(self):
        template = Template(
            '''
            {% extends "base.html" %}
            {% load otree_tags %}
            {% block content %}Click the next button...{% endblock %}
            {% next_button %}
            ''')
        self.assertTrue(check_next_button(template))

    def test_inside_block(self):
        template = Template(
            '''
            {% extends "base.html" %}
            {% load otree_tags %}
            {% block content %}
            Click the next button...
            {% next_button %}
            {% endblock %}
            ''')
        self.assertTrue(check_next_button(template))


class TemplateCheckInSystemCheckTest(TestCase):
    def test_check_fails(self):
        with dummyapp('templatecheckapp') as app_path:
            # Runs without issues.
            with capture_stdout():
                call_command('check')

            template_path = os.path.join(
                app_path,
                'templates',
                'templatecheckapp',
                'broken_template.html')
            with open(template_path, 'w') as f:
                f.write(
                    '''
                    {% extends "base.html" %}

                    This file has dead text.
                    ''')

            try:
                with capture_stdout():
                    call_command('check')
            except CommandError as e:
                message = six.text_type(e)
            else:
                self.fail('Expected check command to fail.')

            # Check for correct app.
            self.assertTrue('templatecheckapp' in message)

            # Check for correct error id.
            self.assertTrue('otree.E005' in message)

            # Check that template name is mentioned.
            path = os.path.join(
                'templatecheckapp',
                'templates',
                'templatecheckapp',
                'broken_template.html')
            self.assertTrue(path in message)

            # Check that dead bits are displayed.
            self.assertTrue('This file has dead text' in message)


class TemplateCheckEncodingTest(TestCase):
    def test_bad_encoding(self):
        file_name = os.path.join(TEST_DIR, 'test_files',
                                 'bad_encoding_template.html')
        self.assertFalse(has_valid_encoding(file_name))

    def test_good_encoding(self):
        file_name = os.path.join(TEST_DIR, 'test_files',
                                 'good_encoding_template.html')
        self.assertTrue(has_valid_encoding(file_name))


class FormatSourceSnippetTest(TestCase):
    def test_unicode_contents(self):
        """
        Testing for the issue described in
        https://github.com/oTree-org/otree-core/issues/408
        """
        source = u'{% formfield player.contribution with label = "好" %}'
        # Should not raise UnicodeEncodeError
        format_source_snippet(source, arrow_position=0)
