import discord
import json
import keyring
import utils.constants as const
import aiohttp
import base64
from utils.config import create_logger, flush
import asyncio
from time import sleep

class VoiceBot(discord.Client):
    def __init__(self, logger, root_data='data', indent=4):
        
        # Allowing my bot to see all members:
        intents = discord.Intents.default()
        intents.members = True

        # To initalize parent class
        super().__init__(intents=intents)

        #Add logger
        self.logger =  logger

        self.root_data=root_data

        self.indent=indent

        self.guild_settings = {}

        self.user_blacklist = []

    async def on_ready(self):
        flush(self, self.root_data, self.indent)
        self.logger.debug('Logged on!')

    async def on_message(self, message):
        # Pass on all bot commands or blacklisted users
        if message.author.bot or message.author.id in self.user_blacklist:
            pass
        else:
            guild_prefix = self.guild_settings[str(message.guild.id)]['prefix']
            if message.content.startswith(guild_prefix) and len(message.content) > len(guild_prefix):
                await self._process_message(message, message.content[len(guild_prefix):])


    # To-do:
        # Find better way to handle the creation + deletion of mp3 files
        # Find a better way to stop the bot from automatically disconnecting (background task?) without blocking other tasks
        # Don't hardcode in commands - create a system of helper functions based on different commands (think - cogs system in discord API)
    async def _process_message(self, message, message_contents):
        split_message = message_contents.split(' ')
        command = split_message[0].upper()
        rest = ' '.join(map(str, split_message[1:]))

        try:
            voice_channel = message.author.voice.channel
        except Exception as e:
            self.logger.error(e)
            voice_channel = None
        if command == 'TTS' and len(rest) < 100 and len(self.voice_clients) == 0 and voice_channel is not None:

            encoded = await self.query_uberduck(rest)

            self.write_base64(encoded)

            await voice_channel.connect()

            source = discord.FFmpegPCMAudio('tts.mp3')

            self.voice_clients[0].play(source, after=None)

            while self.voice_clients[0].is_playing():
                sleep(0.5)

            await self.voice_clients[0].disconnect()
            
    # To-Do: Need some sort of error handling (and move this outside of the main bot class)
    async def query_uberduck(self, text):
        async with aiohttp.ClientSession() as session:
            url = 'https://rtc.uberduck.ai/speak'

            data = '{{"speech":"{0}","voice":"trebek"}}'.format(text)

            async with session.post(url, data=data) as r:
                if r.status == 200:
                    response = await r.read()
                    return response
      
    # To-Do: Move this outside of this class as a helper function for the TTS interface.
    def write_base64(self, response):
        decodedData = base64.b64decode(response)

        with open('tts.mp3', 'wb') as file:
            file.write(decodedData)

creds = keyring.get_password(const.DEFAULT_SERVICE, const.BOT_NAME)
logger = create_logger()
client = VoiceBot(logger=logger)
client.run(creds)