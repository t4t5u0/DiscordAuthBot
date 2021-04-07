import hashlib
import hmac
import time
from datetime import datetime
from hashlib import shake_128


def create_token() -> str:
    t = datetime.timestamp(datetime.now()).__int__().__str__().encode()
    h = hashlib.sha256(t).hexdigest()[:8]
    return h


def compare_token(target1: str, target2: str) -> bool:
    return hmac.compare_digest(target1, target2)
