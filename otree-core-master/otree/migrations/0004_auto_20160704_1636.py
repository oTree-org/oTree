# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import otree.db.models
import otree.common_internal


class Migration(migrations.Migration):

    dependencies = [
        ('otree', '0003_participant__browser_bot_finished'),
    ]

    operations = [
        migrations.AlterField(
            model_name='session',
            name='_anonymous_code',
            field=otree.db.models.CharField(max_length=10, default=otree.common_internal.random_chars_10, null=True, db_index=True),
        ),
    ]
