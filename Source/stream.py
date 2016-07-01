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
def get_channels(channel_list):
    html = webrequest.get_url(twitch.stream_objects() % (','.join(channel_list)))
    json_file = json.loads(html)
    streams = []
    for stream in json_file['streams']:
        streamer = [stream['channel']['url'], stream['channel']['name'] + " - " + stream['channel']['game'], stream['channel']['status'], stream['channel']['logo'], stream['viewers']]
        streams.append(streamer)
    sorted(streams, key=lambda x: x[4])
    items = []
    if len(streams) == 0:
        items.append(workflow.create_item())
    else:
        for streamer in streams:
            items.append(workflow.create_item(
                arg = streamer[0], 
                title = streamer[1], 
                subtitle = streamer[2],
                icon = settings.get_image(streamer[3], streamer[1])))
    workflow.output_items(items)

def get_active_followed_channels():
    channels = settings.get_followers(user_settings)
    get_channels(channels)


def get_followed_channels():
    json_file = settings.load_followed(user_settings['user'])
    items = []
    for follow in json_file['follows']:
        channel = follow['channel']
        items.append(workflow.create_item(
            arg = channel['url'], 
            title = channel['name'], 
            subtitle = channel['game'],
            icon = settings.get_image(channel['logo'], channel['name'])))
    workflow.output_items(items)

def search_games(search):
    html = webrequest.get_url(twitch.search_games() % search)
    json_file = json.loads(html)
    items = []
    for game in json_file['games']:
        game_name = game['name']
        items.append(workflow.create_item(
            arg = game_name, 
            title = game_name, 
            subtitle = "%s Viewers" % game['popularity'],
            icon = settings.get_image(game['box']['small'], game_name)))
    workflow.output_items(items)


def get_top_games():
    html = webrequest.get_url(twitch.top_games())
    json_file = json.loads(html)
    items = []
    for game in json_file['top']:
        game_name = game['game']['name']
        items.append(workflow.create_item(
            arg = game_name, 
            title = game_name, 
            subtitle = "%s Viewers" % game['game']['popularity'],
            icon = settings.get_image(game['game']['box']['small'], game_name)))
    workflow.output_items(items)

def get_videos(channelname):
    html = webrequest.get_url(twitch.videos() % channelname)
    json_file = json.loads(html)
    items = []
    index = 0
    for video in json_file['videos']:
        filename = 'video_preview_%s_%d' % (video['channel']['name'], index)
        icon = None
        if user_settings['enable_previews'] == 'false': icon = 'Images/%s' % channelname
        else: icon = settings.get_image(video['preview'], filename)
        items.append(workflow.create_item(
            arg = video['url'], 
            title = video['title'], 
            subtitle = "%s (%s views)" % (video['created_at'].split('T')[0], video['views']),
            icon = icon))
        index += 1
    workflow.output_items(items)

def get_streams_by_game(gamename):
    html = webrequest.get_url(twitch.streams_per_game() % gamename)
    json_file = json.loads(html)
    items = []
    for stream in json_file['streams']:
        icon = None
        if user_settings['enable_previews'] == 'false': icon = settings.get_image(stream['channel']['logo'], stream['channel']['name'])
        else: icon = settings.get_image(stream['preview']['small'], "video_preview_%s" % stream['channel']['name'])
        items.append(workflow.create_item(
            arg = stream['channel']['url'], 
            title = "%s (%s viewers)" % (stream['channel']['name'], stream['viewers']), 
            subtitle = stream['channel']['status'],
            icon = icon))
    workflow.output_items(items)

def search_streams(term):
    html = webrequest.get_url(twitch.search_channels() % term)
    json_file = json.loads(html)
    items = []
    for channel in json_file['channels']:
        items.append(workflow.create_item(
            arg = channel['url'], 
            title = channel['name'], 
            subtitle = channel['game'],
            icon = settings.get_image(channel['logo'], "video_preview_%s" % channel['name'])))
    workflow.output_items(items)

if __name__ == '__main__':
    #try:
        query_type = sys.argv[1]
        query = sys.argv[2]
        if query_type == 'search_games':
            search_games(query)
        elif query_type == "streams_by_game":
            get_streams_by_game(query)
        elif query_type == "top_games":
            get_top_games()
        elif query_type == "all_followed_channels":
            get_followed_channels()
        elif query_type == 'online_followed_channels':
            get_active_followed_channels()
        elif query_type == "vods":
            get_videos(settings.get_channel(query))
        elif query_type == "search_streams":
            try:
                search_streams(query)
            except:
                workflow.output_items([workflow.create_item()])
        elif query_type == "favorite_streams":
            items = []
            items.append(workflow.create_item(
                arg = "http://www.twitch.tv/%s" % query,
                title = "View Stream for %s" % query,
                subtitle = "Command+Click for VODs"))
            for channel in settings.match_channels(query):
                items.append(workflow.create_item(
                    arg = "http://www.twitch.tv/%s" % channel,
                    title = "%s" % channel,
                    subtitle = "Command+Click for VODs",
                    icon = "Images/%s" % channel))

            workflow.output_items(items)
    #except:
    #    workflow.output_items([workflow.create_item()])


