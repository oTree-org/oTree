# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import otree.db.models


class Migration(migrations.Migration):

    dependencies = [
        ('otree', '0009_browserbotslaunchersessioncode'),
    ]

    operations = [
        migrations.AddField(
            model_name='session',
            name='_bot_case_number',
            field=otree.db.models.PositiveIntegerField(null=True),
        ),
    ]
