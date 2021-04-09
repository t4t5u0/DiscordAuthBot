from pathlib import Path
import configparser

import discord
from discord.ext import commands
from discord.ext.commands import Bot


path = Path.cwd().glob('**/config.ini')
config = configparser.ConfigParser()
config.read(path)
TOKEN = config['TOKEN']['token']

prefix = '!'
bot = Bot(command_prefix=prefix)
bot.load_extension('cog.auth_bot')


@bot.event
async def on_ready():
    print('login')
    await bot.change_presence(activity=discord.Game(f'{prefix}auth 学籍番号 名前'))


if __name__ == "__main__":
    bot.run(TOKEN)
