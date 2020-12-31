import discord
import keyring
import utils.constants as const
import keyring
from utils.config import create_logger

creds = keyring.get_password(const.DEFAULT_SERVICE, const.BOT_NAME)
logger = create_logger()

class VoiceBot(discord.Client):
    def __init__(self, logger):
        
        # Allowing my bot to see all members:
        intents = discord.Intents.default()
        intents.members = True

        # To initalize parent class
        super().__init__(intents=intents)

        #Add logger
        self.logger =  logger

        # Voice Client
        self.voice_client = discord.VoiceClient

    async def on_ready(self):
        self.logger.debug('Logged on!')

    async def on_message(self, message):
        if message.author.id == const.People.bot.value:
            pass
        elif message.content == '!play':
            source = discord.FFmpegPCMAudio(r'nice.mp3')
            self.voice_clients[0].play(source, after=None)
            await message.channel.send('Playing')

        elif message.content == '!join' and len(self.voice_clients) == 0:
            channel = self.get_channel(793956984604196948)
            await channel.connect()

client = VoiceBot(logger)
client.run(creds)