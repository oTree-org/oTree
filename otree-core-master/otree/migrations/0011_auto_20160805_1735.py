# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('otree', '0010_session__bot_case_number'),
    ]

    operations = [
        migrations.RenameField(
            model_name='session',
            old_name='_use_browser_bots',
            new_name='use_browser_bots',
        ),
    ]
