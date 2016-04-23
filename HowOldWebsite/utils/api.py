# -*- coding: UTF-8 -*-

import json

__author__ = 'Hao Yu'


def do_message_maker(success=True, message=None, tip=None):
    return json.dumps({'success': success,
                       'message': message,
                       'tip': tip
                       })
