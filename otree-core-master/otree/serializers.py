#!/usr/bin/env python
# encoding: utf-8

from otree.views.admin import get_all_fields
from rest_framework import serializers
from otree.models import Participant


class ParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participant
        fields = get_all_fields(Participant)
