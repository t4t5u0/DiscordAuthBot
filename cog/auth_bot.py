import configparser
import re
import sys
from pathlib import Path

import discord
# import pandas as pd
from discord import channel
from discord.ext import commands
from libs import libdb, libemail, libmisc, libregex


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
    async def auth(self, ctx: commands.Context, e_mail_address: str):
        "認証メールを飛ばすやつ"
        # private only
        # 無効なアドレスに送信したとき、弾けていない
        if not e_mail_address:
            await ctx.send("メールアドレスを入力してください")
            return
        if not libregex.is_match_regex(self.ptn_list, e_mail_address):
            await ctx.send("不正なメールアドレスです。入力規則を確認してください")
            return
        token = libmisc.create_token()
        e_mail = libemail.create_email(token, e_mail_address, "a")
        result = libemail.send_email(e_mail)
        if result:
            # 仮の処理
            await ctx.send(f"{e_mail_address} にメールを送信しました。"
                           f"次に、`{self.bot.command_prefix}reg token` を叩いてください。"
                           f"メールアドレスに誤りがある場合は、もう一度 `{self.bot.command_prefix}auth email_addr` を叩いてください")
        else:
            await ctx.send("送信失敗")
            # 処理終了
            return
        # メールアドレスを格納する処理をする
        discord_id = ctx.author.id.__str__()
        # insertよりもupsertしたほうがいい気がする
        libdb.db_insert_email(discord_id, e_mail_address)
        # tokenの追加処理。ここもupsertしたほうがいい気がする
        libdb.db_insert_token(e_mail_address, token)

    @commands.command()
    async def reg(self, ctx: commands.Context, token: str):
        discord_id = ctx.author.id.__str__()
        email = libdb.db_get_email_address(discord_id)
        lawtoken = libdb.db_get_token(email)
        if lawtoken == token:
            # 認証ができたら、tokenは消していい
            libdb.db_delete_token(email)
            await ctx.send("認証おっけー")
        else:
            # 認証に失敗したら、失敗カウントをインクリメント
            # 回数もほしいし、副作用を減らしてもいいかなと
            libdb.miss_count_up(discord_id)
            await ctx.send("認証失敗 3回失敗するとトークンが無効化されます")
            


def setup(bot: commands.Bot):
    return bot.add_cog(AuthBotCog(bot))
