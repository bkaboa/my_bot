import discord
import os
import scrapper
import json
from discord.ext import tasks

file = open("config.json", "r+")

configs = json.load(file)
scrap = scrapper.Scrapper()

class Client(discord.Client):
    
    async def on_ready(self):
        for guild in self.guilds:
            for channel_name in configs["discord"]["channels"]:
                if await self.as_channel(guild, channel_name) is False:
                    await self.create_channel(guild, channel_name)
        self.my_loop.start()

    @tasks.loop(seconds=3600)
    async def my_loop(self):
        channels_messages = await scrap.get_messages(configs, file)
        print("Messages: " + str(channels_messages))
        for channel_message in channels_messages:
            channel = discord.utils.get(self.get_all_channels(), name=channel_message[0])
            print("sending message to: " + channel.name + channel_message[0])
            await self.post(channel, channel_message[1])
        print("Sleeping for 60 seconds")
    
    async def as_channel(self, guild, name):
        print("Checking for channel: " + name)
        for guild_channel in guild.channels:
            if name in guild_channel.name:
                return True
        return False

    async def create_channel(self, guild, name):
        channel = await guild.create_text_channel(name)

    async def post(self, channel, message):
        if (message):
            await channel.send(message)
        
    
intents = discord.Intents.default()
intents.message_content = True

client = Client(intents=intents)
client.run(os.environ.get('DISCORD_TOKEN'))
