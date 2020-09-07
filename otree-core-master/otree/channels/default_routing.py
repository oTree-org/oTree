#!/usr/bin/env python
# -*- coding: utf-8 -*-

from channels.routing import route

from otree.channels import consumers


channel_routing = [
    route(
        'websocket.connect', consumers.connect_wait_page,
        path=r'^/wait_page/(?P<params>[\w,]+)/$'),
    route(
        'websocket.disconnect', consumers.disconnect_wait_page,
        path=r'^/wait_page/(?P<params>[\w,]+)/$'),
    route(
        'websocket.connect', consumers.connect_auto_advance,
        path=r'^/auto_advance/(?P<params>[\w,]+)/$'),
    route('websocket.disconnect', consumers.disconnect_auto_advance,
          path=r'^/auto_advance/(?P<params>[\w,]+)/$'),
    route('websocket.connect', consumers.connect_wait_for_session,
          path=r'^/wait_for_session/(?P<pre_create_id>\w+)/$'),
    route('websocket.disconnect', consumers.disconnect_wait_for_session,
          path=r'^/wait_for_session/(?P<pre_create_id>\w+)/$'),
    route('otree.create_session',
          consumers.create_session),
    route('websocket.connect',
          consumers.connect_room_participant,
          path=r'^/wait_for_session_in_room/(?P<params>[\w,]+)/$'),
    route('websocket.disconnect',
          consumers.disconnect_room_participant,
          path=r'^/wait_for_session_in_room/(?P<params>[\w,]+)/$'),
    route('websocket.connect',
          consumers.connect_room_admin,
          path=r'^/room_without_session/(?P<room>\w+)/$'),
    route('websocket.disconnect',
          consumers.disconnect_room_admin,
          path=r'^/room_without_session/(?P<room>\w+)/$'),
    route('websocket.connect',
          consumers.connect_browser_bots_client,
          path=r'^/browser_bots_client/(?P<session_code>\w+)/$'),
    route('websocket.disconnect',
          consumers.disconnect_browser_bots_client,
          path=r'^/browser_bots_client/(?P<session_code>\w+)/$'),
    route('websocket.connect',
          consumers.connect_browser_bot,
          path=r'^/browser_bot_wait/$'),
    route('websocket.disconnect',
          consumers.disconnect_browser_bot,
          path=r'^/browser_bot_wait/$'),

]
