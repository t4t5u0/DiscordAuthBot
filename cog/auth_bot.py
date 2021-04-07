import re
import configparser
from pathlib import Path

import discord
import pandas as pd
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
        self.authed_user_role: int = int(_config['SERVER']['role_id'])
        self.auth_channel: int = int(_config['SERVER']['channel'])

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
            await ctx.send(f"{i:l} {ptn!r}")

    @commands.command()
    async def auth(self, ctx: commands.Context, *, info):
        if ctx.channel.id != self.auth_channel:
            channel: discord.TextChannel = discord.utils.get(
                ctx.guild.channels, id=self.auth_channel)
            await ctx.send(f'{channel.mention}  内で入力してください')
            return

        tmp: list[str] = info.split()
        if len(tmp) == 3:
            # 名字 名前 -> 名字名前
            tmp[1] = ''.join(tmp[1:])
            del tmp[2:]

        if len(tmp) != 2:
            await ctx.send("不正な入力です．入力を見直してください")
            return
        num, name = tmp
        # 下三桁 -1 がインデックスになる
        num = int(num.removeprefix('b')) % 1000 - 1
        df = pd.read_csv('./data.csv', delimiter=',', header=0)
        flag = int(df.at[num, 'flag'])

        if df.at[num, 'name'] != name:
            await ctx.send('不正な入力です．入力を見直してください')
            return
        if flag:
            await ctx.send('あなたはすでに認証されています．問題があった場合，サーバ管理者に連絡してください')
            return

        df.at[num, 'flag'] = 1
        df.to_csv('./data.csv')
        print(df.at[num, 'flag'])
        # self.write_csv(df, num)
        role = discord.utils.find(
            lambda r: r.id == self.authed_user_role, ctx.guild.roles)
        await ctx.author.add_roles(role)
        await ctx.send(f'{ctx.author.mention} は正しく認証されました. Enjoy this server!')

    # @commands.command(hidden=True)
    # async def write_csv(df: pd.DataFrame, num: int):
    #     await print('hoge')
    #     await df.at[num, 'flag'] = 1


def setup(bot: commands.Bot):
    return bot.add_cog(AuthBotCog(bot))


def is_match_regex(ptn_list: list[str], target: str) -> bool:
    for ptn in ptn_list:
        if re.fullmatch(ptn, target):
            return True
    return False
