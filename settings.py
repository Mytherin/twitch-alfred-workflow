
import sqlite3
import webrequest
import json
import twitch

conn = sqlite3.connect('settings.db')
c = conn.cursor()

def default_settings():
    c.execute('INSERT INTO Settings (key,val) VALUES (?,?)', ('user', 'mytherin'))
    c.execute('INSERT INTO Settings (key,val) VALUES (?,?)', ('quality', 'best'))
    c.execute('INSERT INTO Settings (key,val) VALUES (?,?)', ('download_directory', '~/Downloads'))
    c.execute('INSERT INTO Settings (key,val) VALUES (?,?)', ('extra_settings', '--player-no-close --player-passthrough=hls'))
    c.execute('INSERT INTO Settings (key,val) VALUES (?,?)', ('enable_previews', 'false'))
try: 
    # if database is currently empty, instantiate tables with default settings
    c.execute('CREATE TABLE Settings(key STRING, val STRING)')
    c.execute('CREATE TABLE Images(url STRING, filename STRING, cached_time LONGINT)')
    c.execute('CREATE TABLE History(name STRING, popularity INT)')
    default_settings()
    conn.commit()
except:
    pass

def get_settings():
    c.execute('SELECT key,val FROM Settings');
    results = c.fetchall()
    settings = {}
    for tpl in results:
        settings[tpl[0]] = tpl[1]
    return settings

def update_setting(key, val):
    c.execute('SELECT val FROM Settings WHERE key=?', (key,))
    results = c.fetchall()
    if len(results) == 0:
        c.execute('INSERT INTO Settings (key,val) VALUES (?,?)', (key, val))
    else:
        c.execute('UPDATE Settings SET val=? WHERE key=?', (val, key));

def commit():
    conn.commit()

def update_image(url, filename, time):
    c.execute('SELECT cached_time FROM Images WHERE url=?', (url,))
    results = c.fetchall()
    if len(results) == 0:
        c.execute('INSERT INTO Images (url, filename, cached_time) VALUES (?,?,?)', (url, filename, time))
    else:
        c.execute('UPDATE Images SET filename=?, cached_time=? WHERE url=?', (filename, time, url));

def load_image(image_url, filename, time):
    import os
    filename = filename.replace("/", "").replace("\\", "").replace(":", "").replace("'", "").replace('"', "")
    image_data = webrequest.get_url(image_url)
    image_filename = os.path.join('Images', filename)
    f = open(image_filename, 'wb+')
    f.write(image_data)
    f.close()
    update_image(image_url, filename, time)
    conn.commit()
    return image_filename

def get_image(image_url, filename):
    import os
    import time
    current_time = time.time()

    c.execute('SELECT filename, cached_time FROM Images WHERE url=?', (image_url,))
    results = c.fetchall()
    if len(results) == 0 or current_time - results[0][1] < 604800: # invalidate image every week
        return load_image(image_url, filename, current_time)
    else: # cached copy is available
        return os.path.join('Images', results[0][0])

def load_followed(user):
    import time
    current_time = time.time()
    html = webrequest.get_url(twitch.followed_channels() % user)
    json_file = json.loads(html)
    channels = []
    for element in json_file['follows']:
        channels.append(element['channel']['name'])
        add_channel(element['channel']['name'])
    # update cache
    update_setting('followed_channels', '@#@#@'.join(channels))
    update_setting('followed_cache_time', current_time)
    conn.commit()
    return json_file

def load_followed_channels(user, time):
    html = webrequest.get_url(twitch.followed_channels() % user)
    json_file = json.loads(html)
    channels = []
    for element in json_file['follows']:
        channels.append(element['channel']['name'])
        add_channel(element['channel']['name'])
    # update cache
    update_setting('followed_channels', '@#@#@'.join(channels))
    update_setting('followed_cache_time', time)
    conn.commit()
    return channels

def get_followers(settings):
    import time
    current_time = time.time()
    if ('followed_channels' not in settings and 'followed_cache_time' not in settings) or (current_time - int(settings['followed_cache_time']) > 600): # invalidate cache after 10 minutes
        return load_followed_channels(settings['user'], current_time)
    else:
        return settings['followed_channels'].split('@#@#@')

def match_channels(query):
    c.execute('SELECT name FROM History WHERE name LIKE \'%%%s%%\' ORDER BY popularity DESC' % query)
    return [x[0] for x in c.fetchall()]

def add_channel(channel):
    c.execute('SELECT popularity FROM History WHERE name=?', (channel,))
    results = c.fetchall()
    if len(results) == 0:
        c.execute('INSERT INTO History (name, popularity) VALUES (?,?)', (channel, 1))
    else:
        c.execute('UPDATE History SET popularity=? WHERE name=?', (results[0][0] + 1, channel))
    conn.commit()

def get_channel(url):
    if 'twitch.tv/' in url:
        return url.split('twitch.tv/')[1].split('/')[0]
    return url


