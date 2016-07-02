# twitch-alfred-workflow

Alfred Workflow for easily browsing Twitch.tv streams and VODs. To install, download [twitch-livestreamer.alfredworkflow](https://github.com/Mytherin/twitch-alfred-workflow/blob/master/twitch-livestreamer.alfredworkflow) and drag it to your Alfred Workflows. Watching videos requires [Livestreamer](https://github.com/chrippa/livestreamer) to be installed.

## Usage
The main command for opening streams is the `stream` command. Type `stream` followed by the channel name to start viewing a stream. Suggestions will appear based on previous streams you have viewed and based on channels you follow (if you have specified what your Twitch account is).

![Channels](http://i.imgur.com/Yzdkk0y.png)

To view a list of VODs for a specific streamer, hold the `⌘` key and select the streamer to view VODs for. You can then select one of the VODs to view. 

![Streamer VODs](http://i.imgur.com/FphhjIi.png)

## Followed Channels
To view the channels that you follow, you first have to specify your twitch channel. You can do this using the `twitch_channel` command, followed by your username.

![Select Channel](http://i.imgur.com/QFQfZs0.png)

You can view all the channels you are following using the `allfollowed` command. Note that selecting a channel here will open the VOD view, because these channels might not be online.

![All Followed Channels](http://i.imgur.com/VyXHtLj.png)

To only view online followed channels, use the `followed` command. This will display a list of all channels that you follow that are currently streaming.

![Online Followed Channels](http://i.imgur.com/7ay57MO.png)

## Games
You can look at top games on Twitch using the `top` command. 

![Top Games](http://i.imgur.com/3D0nLbZ.png)

You can also search for games with the `games` command. Type in the `games` command and then type the name of the game you are looking for. 

![Search for Games](http://i.imgur.com/50jNgeI.png)

After finding the game you want, select it and you will be presented with a list of online streamers for the specified game.

![Streamers per Game](http://i.imgur.com/Trnnpeu.png)
