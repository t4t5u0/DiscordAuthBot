import re

def is_match_regex(ptn_list: list[str], target: str) -> bool:
    for ptn in ptn_list:
        if re.fullmatch(ptn, target):
            return True
    return False
