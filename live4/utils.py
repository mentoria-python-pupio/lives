import re


def remove_nome_comando(msg: str) -> str:
    pattern = r'/(.*?)(\s|$)'
    result = re.sub(pattern, "", msg, count=1)
    return result