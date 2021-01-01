import logging
import json
import os
import os
import utils.constants as const

def create_logger(logname='UberDuck', default_level=logging.DEBUG, file_name=None, file_level=logging.INFO, format='%(name)s - %(asctime)s - %(levelname)s - %(message)s'):

    # Sets a default logger
    logger = logging.getLogger(logname)
    logger.setLevel(default_level)

    formatter = logging.Formatter(format)

    stream_hander = logging.StreamHandler()
    stream_hander.setFormatter(formatter)

    logger.addHandler(stream_hander)
    
    if file_name is not None:
        file_handler = logging.FileHandler(file_name)
        file_handler.setLevel(file_level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger

def flush(bot, root_data='data',indent=4):
    """
        Imports all data files and cache's values. Also removes
    """
    bot.logger.debug('Flushing!')

    # Creates a data file to hold various settings
    if not os.path.exists(root_data):
        os.makedirs(root_data)

        bot.logger.debug('Creating data dir')

    #####################
    # Loads guild settings
    ####################
    guildsettingsfile = r'{}\guildsettings.json'.format(root_data)
    
    # If the file doesn't exist - make one (assume every guild is default settings)
    if not os.path.isfile(guildsettingsfile):

        bot.logger.debug('Creating guild settings')

        bot.guild_settings = {}
        for guild in bot.guilds:
            bot.guild_settings[str(guild.id)] = {'prefix':const.DEFAULT_PREFIX}
            
        with open(guildsettingsfile, 'w') as f:
            json.dump(bot.guild_settings, f, indent=indent)

    #Otherwise open the file - and add any new guilds to the file
    else:
        with open(guildsettingsfile, 'r') as f:
            bot.guild_settings = json.load(f)
        
        for guild in bot.guilds:
            if str(guild.id) not in bot.guild_settings:
                bot.guild_settings[guild.id] = {'prefix':const.DEFAULT_PREFIX}

        with open(guildsettingsfile, 'w') as f:
            json.dump(bot.guild_settings, f, indent=indent)
    

    #####################
    # Loads blacklisted users
    ####################
    userblacklistfile = r'{}\userblacklist.json'.format(root_data)

    # If there isn't a user blacklist then make one
    if not os.path.isfile(userblacklistfile):
        bot.logger.debug('Creating blacklist')

        bot.user_blacklist = []
            
        with open(userblacklistfile, 'w') as f:
            json.dump(bot.user_blacklist, f, indent=indent)

    #Otherwise open the file
    else:
        with open(userblacklistfile, 'r') as f:
            bot.user_blacklist = json.load(f)
