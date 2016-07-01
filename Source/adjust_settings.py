#!/usr/bin/env python
# encoding: utf-8
#
# Copyright  (c) 2016 mark.raasveldt@gmail.com
#
# MIT Licence. See http://opensource.org/licenses/MIT
#
# Created on 2016-06-29
#

import sys
import json
import workflow
import webrequest
import os
import twitch
import settings

user_settings = settings.get_settings()

items = []
if sys.argv[1] == 'toggle_previews':
    if user_settings['enable_previews'] == 'false':
        items.append(workflow.create_item(
            arg = "enable_previews:true",
            title = "Enable Preview Images",
            subtitle = "Show preview images on VODs and streams."))
    else:
        items.append(workflow.create_item(
            arg = "enable_previews:false",
            title = "Disable Preview Images",
            subtitle = "Show channel image on VODs and streams."))
elif sys.argv[1] == 'set_twitch_channel':
    items.append(workflow.create_item(
        arg = "user:%s" % sys.argv[2],
        title = "Set Twitch Channel To %s" % sys.argv[2],
        subtitle = "Twitch channel name is used for browsing followed streams."))
elif sys.argv[1] == 'adjust_settings':
    spl = sys.argv[2].split(':')
    settings.update_setting(spl[0], spl[1])
    settings.commit()
    exit()

workflow.output_items(items)
