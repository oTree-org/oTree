# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import otree.db.models


class Migration(migrations.Migration):

    dependencies = [
        ('otree', '0002_browserbotsubmit_is_last'),
    ]

    operations = [
        migrations.AddField(
            model_name='participant',
            name='_browser_bot_finished',
            field=otree.db.models.BooleanField(default=False, choices=[(True, 'Yes'), (False, 'No')]),
        ),
    ]
