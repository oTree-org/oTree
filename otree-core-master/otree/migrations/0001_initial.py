# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import otree.common_internal
import otree.models.varsmixin
import otree.db.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BrowserBotSubmit',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('page_class_dotted', models.CharField(max_length=200)),
                ('param_dict', otree.db.models.JSONField(null=True)),
                ('input_is_valid', models.BooleanField()),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='CompletedGroupWaitPage',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('page_index', models.PositiveIntegerField()),
                ('group_pk', models.PositiveIntegerField()),
                ('after_all_players_arrive_run', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='CompletedSubsessionWaitPage',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('page_index', models.PositiveIntegerField()),
                ('after_all_players_arrive_run', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='ExpectedRoomParticipant',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('room_name', models.CharField(max_length=50)),
                ('participant_label', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='FailedSessionCreation',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('pre_create_id', models.CharField(db_index=True, max_length=100)),
                ('message', models.CharField(max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='GlobalSingleton',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('locked', otree.db.models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], default=False)),
            ],
        ),
        migrations.CreateModel(
            name='PageCompletion',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('app_name', models.CharField(max_length=300)),
                ('page_index', models.PositiveIntegerField()),
                ('page_name', models.CharField(max_length=300)),
                ('time_stamp', models.PositiveIntegerField()),
                ('seconds_on_page', models.PositiveIntegerField()),
                ('subsession_pk', models.PositiveIntegerField()),
                ('auto_submitted', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='PageTimeout',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('page_index', models.PositiveIntegerField()),
                ('expiration_time', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Participant',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('vars', otree.db.models.JSONField(default=dict, null=True)),
                ('exclude_from_data_analysis', otree.db.models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], default=False)),
                ('time_started', otree.db.models.DateTimeField(null=True)),
                ('mturk_assignment_id', otree.db.models.CharField(max_length=50, null=True)),
                ('mturk_worker_id', otree.db.models.CharField(max_length=50, null=True)),
                ('start_order', otree.db.models.PositiveIntegerField(db_index=True, null=True)),
                ('label', otree.db.models.CharField(max_length=50, null=True)),
                ('_index_in_subsessions', otree.db.models.PositiveIntegerField(default=0, null=True)),
                ('_index_in_pages', otree.db.models.PositiveIntegerField(db_index=True, null=True, default=0)),
                ('id_in_session', otree.db.models.PositiveIntegerField(null=True)),
                ('_waiting_for_ids', otree.db.models.CharField(max_length=300, null=True)),
                ('code', otree.db.models.CharField(default=otree.common_internal.random_chars_8, max_length=16, null=True, unique=True)),
                ('last_request_succeeded', otree.db.models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], verbose_name='Health of last server request')),
                ('visited', otree.db.models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], db_index=True, default=False)),
                ('ip_address', otree.db.models.GenericIPAddressField(null=True)),
                ('_last_page_timestamp', otree.db.models.PositiveIntegerField(null=True)),
                ('_last_request_timestamp', otree.db.models.PositiveIntegerField(null=True)),
                ('is_on_wait_page', otree.db.models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], default=False)),
                ('_current_page_name', otree.db.models.CharField(max_length=200, verbose_name='page', null=True)),
                ('_current_app_name', otree.db.models.CharField(max_length=200, verbose_name='app', null=True)),
                ('_round_number', otree.db.models.PositiveIntegerField(null=True)),
                ('_current_form_page_url', otree.db.models.URLField(null=True)),
                ('_max_page_index', otree.db.models.PositiveIntegerField(null=True)),
                ('_is_auto_playing', otree.db.models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], default=False)),
            ],
            options={
                'ordering': ['pk'],
            },
            bases=(otree.models.varsmixin._SaveTheChangeWithCustomFieldSupport, models.Model),
        ),
        migrations.CreateModel(
            name='ParticipantLockModel',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('participant_code', models.CharField(max_length=16, unique=True)),
                ('locked', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='ParticipantRoomVisit',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('room_name', models.CharField(max_length=50)),
                ('participant_label', models.CharField(max_length=200)),
                ('tab_unique_id', models.CharField(max_length=20, unique=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='ParticipantToPlayerLookup',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('page_index', models.PositiveIntegerField()),
                ('app_name', models.CharField(max_length=300)),
                ('player_pk', models.PositiveIntegerField()),
                ('url', models.CharField(max_length=300)),
                ('participant', models.ForeignKey(to='otree.Participant')),
            ],
        ),
        migrations.CreateModel(
            name='RoomToSession',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('room_name', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('vars', otree.db.models.JSONField(default=dict, null=True)),
                ('config', otree.db.models.JSONField(default=dict, null=True)),
                ('label', otree.db.models.CharField(help_text='For internal record-keeping', blank=True, max_length=300, null=True)),
                ('experimenter_name', otree.db.models.CharField(help_text='For internal record-keeping', blank=True, max_length=300, null=True)),
                ('code', otree.db.models.CharField(default=otree.common_internal.random_chars_8, max_length=16, null=True, unique=True)),
                ('time_scheduled', otree.db.models.DateTimeField(help_text='For internal record-keeping', blank=True, null=True)),
                ('time_started', otree.db.models.DateTimeField(null=True)),
                ('mturk_HITId', otree.db.models.CharField(help_text='Hit id for this session on MTurk', blank=True, max_length=300, null=True)),
                ('mturk_HITGroupId', otree.db.models.CharField(help_text='Hit id for this session on MTurk', blank=True, max_length=300, null=True)),
                ('mturk_qualification_type_id', otree.db.models.CharField(help_text='Qualification type that is assigned to each worker taking hit', blank=True, max_length=300, null=True)),
                ('mturk_num_participants', otree.db.models.IntegerField(help_text='Number of participants on MTurk', default=-1, null=True)),
                ('mturk_sandbox', otree.db.models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], help_text='Should this session be created in mturk sandbox?', default=True)),
                ('archived', otree.db.models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], db_index=True, default=False)),
                ('comment', otree.db.models.TextField(blank=True, null=True)),
                ('_anonymous_code', otree.db.models.CharField(db_index=True, max_length=8, null=True, default=otree.common_internal.random_chars_10)),
                ('special_category', otree.db.models.CharField(db_index=True, max_length=20, null=True)),
                ('_pre_create_id', otree.db.models.CharField(db_index=True, max_length=300, null=True)),
                ('_use_browser_bots', otree.db.models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], default=False)),
            ],
            options={
                'ordering': ['pk'],
            },
            bases=(otree.models.varsmixin._SaveTheChangeWithCustomFieldSupport, models.Model),
        ),
        migrations.CreateModel(
            name='StubModel',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
            ],
        ),
        migrations.AddField(
            model_name='roomtosession',
            name='session',
            field=models.ForeignKey(to='otree.Session'),
        ),
        migrations.AddField(
            model_name='participant',
            name='session',
            field=otree.db.models.ForeignKey(to='otree.Session'),
        ),
        migrations.AddField(
            model_name='pagetimeout',
            name='participant',
            field=models.ForeignKey(to='otree.Participant'),
        ),
        migrations.AddField(
            model_name='pagecompletion',
            name='participant',
            field=models.ForeignKey(to='otree.Participant'),
        ),
        migrations.AddField(
            model_name='pagecompletion',
            name='session',
            field=models.ForeignKey(to='otree.Session'),
        ),
        migrations.AlterUniqueTogether(
            name='expectedroomparticipant',
            unique_together=set([('room_name', 'participant_label')]),
        ),
        migrations.AddField(
            model_name='completedsubsessionwaitpage',
            name='session',
            field=models.ForeignKey(to='otree.Session'),
        ),
        migrations.AddField(
            model_name='completedgroupwaitpage',
            name='session',
            field=models.ForeignKey(to='otree.Session'),
        ),
        migrations.AddField(
            model_name='browserbotsubmit',
            name='participant',
            field=models.ForeignKey(to='otree.Participant'),
        ),
        migrations.AddField(
            model_name='browserbotsubmit',
            name='session',
            field=models.ForeignKey(to='otree.Session'),
        ),
        migrations.AlterUniqueTogether(
            name='participanttoplayerlookup',
            unique_together=set([('participant', 'page_index')]),
        ),
        migrations.AlterIndexTogether(
            name='participanttoplayerlookup',
            index_together=set([('participant', 'page_index')]),
        ),
        migrations.AlterIndexTogether(
            name='participant',
            index_together=set([('session', 'mturk_worker_id', 'mturk_assignment_id')]),
        ),
        migrations.AlterIndexTogether(
            name='pagetimeout',
            index_together=set([('participant', 'page_index')]),
        ),
        migrations.AlterUniqueTogether(
            name='completedsubsessionwaitpage',
            unique_together=set([('page_index', 'session')]),
        ),
        migrations.AlterIndexTogether(
            name='completedsubsessionwaitpage',
            index_together=set([('page_index', 'session')]),
        ),
        migrations.AlterUniqueTogether(
            name='completedgroupwaitpage',
            unique_together=set([('page_index', 'session', 'group_pk')]),
        ),
        migrations.AlterIndexTogether(
            name='completedgroupwaitpage',
            index_together=set([('page_index', 'session', 'group_pk')]),
        ),
    ]
