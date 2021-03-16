from pathlib import Path
import configparser

import discord
from discord.ext import commands
from discord.ext.commands import Bot


path = Path.cwd().glob('**/config.ini')
config = configparser.ConfigParser()
config.read(path)
TOKEN = config['TOKEN']['token']

prefix = '/'
bot = Bot(command_prefix=prefix)
bot.load_extension('cog.auth_bot')


if __name__ == "__main__":
    bot.run(TOKEN)