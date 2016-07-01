
def followed_channels(): 
	return "https://api.twitch.tv/kraken/users/%s/follows/channels?limit=25"
def stream_objects(): 
	return "https://api.twitch.tv/kraken/streams?channel=%s"
def videos(): 
	return "https://api.twitch.tv/kraken/channels/%s/videos?limit=25&broadcasts=true&hls=true"
def top_games(): 
	return "https://api.twitch.tv/kraken/games/top?limit=25"
def search_streams(): 
	return "https://api.twitch.tv/kraken/search/streams?q=%s"
def search_games(): 
	return "https://api.twitch.tv/kraken/search/games?q=%s&type=suggest"
def search_channels(): 
	return "https://api.twitch.tv/kraken/search/channels?q=%s"
def streams_per_game():
	return "https://api.twitch.tv/kraken/streams?game=%s"
