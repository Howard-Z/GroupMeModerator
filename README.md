# GroupMeModerator
A simple user moderation bot for Bruin Club Tennis

## Setup

Setting up a bot instance of your own is pretty easy. First things first is to get an api token from [GroupMe](https://dev.groupme.com/)

You will need a URL (IP) to use the callback so I recommend using a dynamic DNS (DDNS) service like Dynu to generate a domain to point your bot to. After that, you will probably have to port forward your application to be visible to the internet

After that you create a bot by filling out their form [here](https://dev.groupme.com/bots/new)

Once you have done this taken note of your `Access Token` and your `Bot ID`

Note that Bot IDs are on a per group chat basis so if you have the same bot script running

## Running
`python3 main.py --file "file/path/here --id BOT_ID_HERE --token YOUR_API_TOKEN`