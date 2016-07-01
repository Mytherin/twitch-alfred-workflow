#!/usr/bin/env python
# encoding: utf-8

import os

def sanitize_input(inp):
	if inp == None: return inp
	return inp.replace("\"", "").replace("'", "")

def create_item(arg = "http://www.twitch.tv", title = "Sorry.", subtitle = "No Streamers Found.", icon = None):
    return u"""
{
	"title": "%s",
	"subtitle": "%s",
	"icon": {
	   "path": "%s"
	},
	"arg": "%s"
},""" % (sanitize_input(title), sanitize_input(subtitle), "icon.png" if icon == None else sanitize_input(icon), sanitize_input(arg))

def output_items(items):
    print('{ "items": [')
    for item in items:
    	print(item.encode('utf-8'))
    print("]}")