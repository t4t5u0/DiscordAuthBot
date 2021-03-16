# DiscordAuthBot

学籍番号と名前の組をもとに簡易認証を行うBotです．
データは手動で作成する必要があります．

将来的には，メールに認証フレーズを送信し，それをもとに認証する形に変更します．


## Usage 
1. [Discord Developer Portal — My Applications](https://discord.com/developers/applications) でBotを作成し，Botのトークンを取得します

1.
    ```bash
    $ git clone https://github.com/t4t5u0/DiscordAuthBot
    $ cd DiscordAuthBot
    ```
1. config.ini にBotのトークンと，認証用のロールID，認証を受け付けるチャンネルを書き込みます

1. data.csv にデータを書き込みます．各データの間には空白を入れないようにしてください．

1. 
    ```bash
    $ nohup python main.py &
    ```
    などで起動します
