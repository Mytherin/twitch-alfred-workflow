#!/usr/bin/env python
# encoding: utf-8
#
# Copyright  (c) 2016 mark.raasveldt@gmail.com
#
# MIT Licence. See http://opensource.org/licenses/MIT
#
# Created on 2016-06-29
#

import os
import settings
import sys
import subprocess

user_settings = settings.get_settings()
livestream_url = sys.argv[1]
livestreamer = 'livestreamer'

potential_livestream_locations = [
	'/usr/bin/livestreamer',
	'/usr/local/bin/livestreamer',
	'/opt/bin/livestreamer',
	'/opt/local/bin/livestreamer']

for location in potential_livestream_locations:
	if os.path.isfile(location):
		livestreamer = location
		break

if 'livestreamer' in user_settings:
	livestreamer = user_settings['livestreamer']

quality = "best"
if 'quality' in user_settings:
	quality = user_settings['quality']

extra_settings = []
if 'extra_settings' in user_settings:
	extra_settings = user_settings['extra_settings'].split(' ')

channel = settings.get_channel(livestream_url)
settings.add_channel(channel)


import subprocess
subprocess.Popen([livestreamer, livestream_url, quality] + extra_settings)