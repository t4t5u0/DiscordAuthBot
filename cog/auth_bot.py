import re
import configparser
from pathlib import Path

import discord
# import pandas as pd
from discord import channel
from discord.ext import commands


class AuthBotCog(commands.Cog, name="auth"):
    """
    Botのメイン部分
    !auth bxxxxxxx 名前
    """

    def __init__(self, bot: commands.Bot) -> None:
        _path = Path.cwd().glob('**/config.ini')
        _config = configparser.ConfigParser()
        _config.read(_path)

        self.bot = bot
        # self.authed_user_role: int = int(_config['SERVER']['role_id'])
        # self.auth_channel: int = int(_config['SERVER']['channel'])

        self.ptn_list: list[str] = []

    @commands.command()
    async def add_email(self, ctx: commands.Context, ptn: str):
        self.ptn_list.append(ptn)
        await ctx.send(f"規則 `{ptn!r}` を登録しました")

    @commands.command()
    async def rm_email(self, ctx: commands.Context, num: int):
        if len(self.ptn_list) > num:
            await ctx.send(f"規則{num} は存在しません")
            return
        ptn = self.ptn_list[num]
        await ctx.send(f"規則{num}, `{ptn!r}` を削除しました")

    @commands.command()
    async def show_email(self, ctx: commands.Context):
        await ctx.send("メールアドレス規則一覧")
        for i, ptn in enumerate(self.ptn_list):
            l = len(str(i))
            await ctx.send(f"{i:{l}} {ptn!r}")

    @commands.command()
    async def auth(self, ctx: commands.Context, *, info):
        # private only
        # 

        pass


def setup(bot: commands.Bot):
    return bot.add_cog(AuthBotCog(bot))

