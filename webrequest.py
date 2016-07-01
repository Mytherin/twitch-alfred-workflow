

import urllib2

def get_url(url):
	if url == None: return "{}"
	url = url.replace(" ", "+")
	response = urllib2.urlopen(url)
	return str(response.read())
