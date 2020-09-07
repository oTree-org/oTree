#!/usr/bin/env python
# encoding: utf-8

from django.views.generic import View
from django.http import JsonResponse
from django.http import Http404

from rest_framework import generics, permissions

from otree.models import Session
from otree.serializers import ParticipantSerializer


class Ping(View):

    def get(self, request):
        response = JsonResponse({"ping": True})
        response["Access-Control-Allow-Origin"] = "*"
        return response


class SessionParticipantsList(generics.ListCreateAPIView):
    serializer_class = ParticipantSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        session_code = self.kwargs['session_code']
        try:
            session = Session.objects.get(code=session_code)
        except Session.DoesNotExist:
            raise Http404('This session no longer exists.')
        return session.get_participants()
