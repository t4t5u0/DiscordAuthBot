from pathlib import Path
import configparser

import discord
from discord.ext import commands
from discord.ext.commands import Bot

def main():

    path = Path.cwd().glob('**/config.ini')
    config = configparser.ConfigParser()
    config.read(path)
    TOKEN = config['TOKEN']['token']

    prefix = '/'
    bot = Bot(command_prefix=prefix)
    bot.load_extension('cog.auth_bot')

    @bot.event
    async def on_ready():
        print('login')
        await bot.change_presence(activity=discord.Game('!auth 学籍番号 名前')) 

    bot.run(TOKEN)


if __name__ == "__main__":
    main()