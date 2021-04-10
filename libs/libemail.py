import configparser
import smtplib
from email.mime.text import MIMEText
from email.utils import formatdate
from pathlib import Path

# 例えば、送信元がgmailの場合、事前に認証が必要
# 認証の確認をする関数が欲しい
# 特性上、複数サーバでの運用が難しい
# 送信側のメールアドレスを用意することで、一応複数サーバはいける
# どのサーバに対する認証かがわからず、難しくなるかもしれない
# あるUserが参加してるサーバと、Botが参加してるサーバについて交叉を取ることで、いい感じにできそうではある

path = Path.cwd().glob('**/config.ini')
config = configparser.ConfigParser()
config.read(path)
FROM_ADDR = config['EMAIL']['from']
PASS = config['EMAIL']['pass']


def create_email(token: str, to_addr: str, server_name: str) -> MIMEText:
    "メールを生成"
    msg = MIMEText(
        'こんにちは。DiscordAuthBotです。\n\n'
        f'このメールは、{server_name} にて、ユーザを認証するためのものです。'
        '下記のトークンをBotのDMで入力してください。なお。このトークンの有効期間は1時間です。これを過ぎた場合は、再発行してください\n'
        '例) /auth ThisIsToken\n\n'
        f'{token} \n\n'
        '※ このメールに覚えのない方へ\n'
        '他のユーザが誤ってメールアドレスを入力した可能性があります。お手数ですが、破棄していただくようお願いします。'
    )
    msg['Subject'] = f'Disocrd サーバ {server_name} 認証確認メール'
    msg['From'] = FROM_ADDR
    msg['To'] = to_addr
    msg['Date'] = formatdate()
    return msg


def send_email(to_addr: str, body_msg: MIMEText) -> bool:
    smtpobj = smtplib.SMTP('smtp.gmail.com', 587)
    # smtpobj.ehlo()
    smtpobj.starttls()
    # smtpobj.ehlo()
    smtpobj.login(FROM_ADDR, PASS)
    # (235, b'2.7.0 Accepted')

    # ?try-exception する？
    try:
        smtpobj.sendmail(FROM_ADDR, to_addr, body_msg.as_string())
        smtpobj.close()
        return True
    except:
        # 実装めんどくなったから、これで
        # 後でちゃんと作るかも
        return False
    