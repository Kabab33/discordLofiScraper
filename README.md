# Discord Lofi scraper

A simple python app to get data from discord lofi and put it in a json file at the same location as the `__main__.py` file.


# Configuration
First of all you want to coppy the .env.example to .env

To get the `DISCORD_ACTIVITY_TOKEN` and `DISCORD_SAYS_URL` you need to open your network tab in the inspector.

1. Open Discord and start the lofi activity.
2. In the network tab, filter by json.
3. Click the garbage icon in the top left corner.
4. Skip to the next song.
5. There shuld be a reuest with the file as `1?seed=XXXXXXXXXX`.
6. Copy the url of that request and paste it in the `.env` file as `DISCORD_SAYS_URL`.
7. Then go to the request headers and look for `authorization`.
8. Copy the value of the `authorization` header and paste it in the `.env` file as `DISCORD_ACTIVITY_TOKEN`.
9. Pause the lofi activity song.

It shuold now work however the token wille expire after a while.
Simply repeat the steps above to get a new token and update the `.env` file.
There are some other options in the `.env` file you can change to your liking.
especially the `PLAYLIST`, `SONGS` and `START_WITH` options.