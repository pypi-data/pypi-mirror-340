# -*- coding:utf-8 -*-

import json

from aigc_intent_solt.scene_config import scene_prompts
from aigc_intent_solt.utils.date_utils import get_current_date
from aigc_intent_solt.utils.helpers import get_slot_query_user_json, get_slot_update_json


def get_slot_update_message(scene_name, dynamic_example, slot_template, user_input, session_id):
    message = scene_prompts.slot_update.format(scene_name, get_current_date(), dynamic_example, json.dumps(get_slot_update_json(slot_template, session_id), ensure_ascii=False), user_input)
    return message


def get_slot_query_user_message(scene_name, slot, user_input, session_id):
    message = scene_prompts.slot_query_user.format(scene_name, json.dumps(get_slot_query_user_json(slot, session_id), ensure_ascii=False), user_input)
    return message
