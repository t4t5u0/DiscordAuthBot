import hashlib
import hmac
import time
from datetime import datetime
from hashlib import shake_128


def create_token(n=8) -> str:
    "n桁のトークンを発行する関数"
    t = datetime.timestamp(datetime.now()).__int__().__str__().encode()
    h = hashlib.sha256(t).hexdigest()[:n]
    return h


def compare_token(target1: str, target2: str) -> bool:
    "トークンを比較する関数"
    return hmac.compare_digest(target1, target2)
