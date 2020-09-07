# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('otree', '0008_auto_20160728_1916'),
    ]

    operations = [
        migrations.CreateModel(
            name='BrowserBotsLauncherSessionCode',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('code', models.CharField(max_length=10)),
                ('is_only_record', models.BooleanField(unique=True, default=True)),
            ],
        ),
    ]
