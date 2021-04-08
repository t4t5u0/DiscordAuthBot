from pathlib import Path

import sqlite3


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
            time        INTEGER,
            miss_count  INTEGER
        );
    """
    conn = db_connection()
    conn.execute(db1)
    conn.execute(db2)
    conn.commit()
    conn.close()


def db_insert_email():
    pass


def db_delete_email():
    pass


def db_insert_token():
    pass


def db_delete_token():
    pass
