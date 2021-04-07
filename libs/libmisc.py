import time
from hashlib import shake_128
from datetime import datetime


def create_token() -> str:
    t = datetime.timestamp(datetime.now()).__int__().__str__()
    pass

def compare_token():
    pass
