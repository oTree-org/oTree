#!/usr/bin/env python
# -*- coding: utf-8 -*-
from typing import List
import otree.models

class WaitPage:
    wait_for_all_groups = False
    title_text = None
    body_text = None
    template_name = None
    round_number = None  # type: int
    participant = None  # type: otree.models.Participant
    session = None  # type: otree.models.Session

    def is_displayed(self) -> bool: pass
    def after_all_players_arrive(self): pass


class Page:
    round_number = None  # type: int
    template_name = None # type: str
    timeout_seconds = None # type: int
    timeout_submission = None # type: dict
    timeout_happened = None # type: bool
    participant = None  # type: otree.models.Participant
    session = None  # type: otree.models.Session
    form_model = None #
    form_fields = None  # type: List[str]

    def get_form_fields(self) -> List['str']: pass
    def vars_for_template(self) -> dict: pass
    def before_next_page(self): pass
    def is_displayed(self) -> bool: pass
