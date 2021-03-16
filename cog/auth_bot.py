import discord
from discord import channel
from discord.ext import commands
import pandas as pd


class AuthBotCog(commands.Cog, name="auth"):
    """
    Botのメイン部分
    !auth bxxxxxxx 名前
    """

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.authed_user_role = 821195739492515853 # id をコピーする
        self.auth_channel = 821195590008307773 # id をコピーする

    @commands.command()
    async def auth(self, ctx: commands.Context, *, info):
        if ctx.channel.id != self.auth_channel:
            channel: discord.TextChannel = discord.utils.get(
                ctx.guild.channels, id=self.auth_channel)
            await ctx.send(f'{channel.mention}  内で入力してください')
            return
        tmp = info.split()
        if len(tmp) != 2:
            await ctx.send("不正な入力です．入力を見直してください")
            return
        num, name = tmp
        # 下三桁 -1 がインデックスになる
        num = int(num) % 1000 - 1 
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

