#!/usr/bin/env python
# -*- coding: utf-8 -*-


# =============================================================================
# IMPORTS
# =============================================================================

from django.utils.translation import ugettext_lazy

# =============================================================================
# CONSTANTS
# =============================================================================

SubsessionClass = 'SubsessionClass'
GroupClass = 'GroupClass'
PlayerClass = 'PlayerClass'
UserClass = 'UserClass'

group_id = 'group_id'

user_code = 'user_code'
subsession_code = 'subsession_code'
subsession_code_obfuscated = 'exp_code'

nickname = 'nickname'

completed_views = 'completed_views'

form_invalid = 'form_invalid'
precondition = 'precondition'
mturk_worker_id = 'mturk_worker_id'
debug_values_built_in = 'debug_values_built_in'
debug_values = 'debug_values'
get_param_truth_value = '1'

admin_secret_code = 'admin_secret_code'
timeout_seconds = 'timeout_seconds'
timeout_happened = 'timeout_happened'
check_auto_submit = 'check_auto_submit'
page_expiration_times = 'page_timeouts'
participant_label = 'participant_label'
participant_id = 'participant_id'
participant_code = 'participant_code'
session_id = 'session_id'
session_code = 'session_code'
wait_page_http_header = 'oTree-Wait-Page'
redisplay_with_errors_http_header = 'oTree-Redisplay-With-Errors'
user_type = 'user_type'
user_type_participant = 'p'
success = True
failure = False


# Translators: for required form fields
field_required_msg = ugettext_lazy('This field is required.')

AUTO_NAME_BOTS_EXPORT_FOLDER = 'auto_name'