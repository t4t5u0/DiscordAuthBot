import sqlite3
from pathlib import Path
from datetime import datetime


def db_connection() -> sqlite3.Connection:
    "閉じ忘れないように"
    path = Path.cwd().glob('**/info.db')
    db_name = str(list(path)[0])
    conn = sqlite3.connect(db_name, detect_types=sqlite3.PARSE_DECLTYPES)
    return conn


def db_create():
    db1 = """
        CREATE TABLE IF NOT EXISTS e-mail_table (
            discord_id  TEXT PRIMARY KEY,
            e-mail      TEXT
        );
    """

    db2 = """
        CREATE TABLE IF NOT EXISTS token_table(
            e-mail      TEXT PRIMARY KEY,
            token       TEXT,
            created_at  INTEGER,
            miss_count  INTEGER
        );
    """
    conn = db_connection()
    conn.execute(db1)
    conn.execute(db2)
    conn.commit()
    conn.close()


def db_insert_email(discord_id: str, email: str):
    query = "INSERT INTO e-mail_table VALUES(?, ?)"

    conn = db_connection()
    conn.execute(query, (discord_id, email))
    conn.commit()
    conn.close()


def db_delete_email(discord_id: str):
    query = "DELETE FROM e-mail_table WHERE discord_id = ?"
    conn = db_connection()
    conn.execute(query, (discord_id,))
    conn.commit()
    conn.close()


def db_insert_token(email: str, token: str):
    query = "INSERT INTO token_table VALUES(?, ?, ?, ?)"
    created_at = datetime.timestamp(datetime.now()).__int__()
    miss_count = 0
    conn = db_connection()
    conn.execute(query, (email, token, created_at, miss_count))
    conn.close()


def db_delete_token(email: str):
    query = "DELETE FROM e_mail_table WHERE email = ?"
    conn = db_connection()
    conn.execute(query, email)
    conn.commit()
    conn.close()


def miss_count_up(discord_id: str):
    pass
